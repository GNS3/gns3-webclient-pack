#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 GNS3 Technologies Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import subprocess
import shlex
import psutil
import urllib.parse
import datetime

try:
    from gns3_webclient_pack.qt import QtCore, QtGui, QtWidgets, QtNetwork
except ImportError:
    raise SystemExit("Can't import Qt modules: Qt and/or PyQt is probably not installed correctly...")

from gns3_webclient_pack.local_config import LocalConfig
from gns3_webclient_pack.settings import COMMANDS_SETTINGS, CONTROLLER_SETTINGS
from gns3_webclient_pack.version import __version__
from gns3_webclient_pack.utils.bring_to_front import bring_window_to_front_from_pid
from gns3_webclient_pack.application import Application
from gns3_webclient_pack.main import checks
from gns3_webclient_pack.launcher_error import LauncherError
from gns3_webclient_pack.pcap_stream import PcapStream

import logging
log = logging.getLogger(__name__)


class Command(object):

    def __init__(self, host, port, path, params, url):

        self._host = host
        self._port = port
        self._path = path
        self._params = params
        self._url = url

    @staticmethod
    def gnome_terminal_env():

        uid = os.getuid()

        # get list of processes of current user
        procs = [p.info for p in psutil.process_iter(
            attrs=['name', 'pid', 'ppid', 'create_time', 'uids']
        ) if p.info['uids'].real == uid]

        # get pid of gnome-terminal-server process
        gnome_terminal_server_pid = [p['pid'] for p in procs if p['name'] == "gnome-terminal-server"]
        if not gnome_terminal_server_pid:
            return {}
        gnome_terminal_server_pid = gnome_terminal_server_pid[0]

        # get subprocesses of gnome-terminal-server
        gnome_terminal_server_children = [p for p in procs if p['ppid'] == gnome_terminal_server_pid]
        gnome_terminal_server_children.sort(key=lambda p: p['create_time'], reverse=True)

        # return the gnome-terminal environment variables of the first subprocess named telnet
        for proc in gnome_terminal_server_children:
            if proc['name'] == "telnet":
                try:
                    env = psutil.Process(proc['pid']).environ()
                    if 'GNOME_TERMINAL_SERVICE' in env and \
                            'GNOME_TERMINAL_SCREEN' in env:
                        return {'GNOME_TERMINAL_SERVICE': env['GNOME_TERMINAL_SERVICE'],
                                'GNOME_TERMINAL_SCREEN': env['GNOME_TERMINAL_SCREEN']}
                except psutil.Error:
                    pass
        return {}

    def _exec_command(self, command):
        """
        Execute a command using subprocess

        :param command: command with all variables replaced
        """

        if sys.platform.startswith("win"):
            # use the string on Windows
            process = subprocess.call(command, env=os.environ)
        else:
            # use arguments on other platforms
            try:
                args = shlex.split(command)
            except ValueError as e:
                raise LauncherError("Cannot parse '{}': {}".format(command, e))

            env = os.environ.copy()
            # special case to force gnome-terminal to correctly use tabs on Linux
            if sys.platform.startswith("linux") and "gnome-terminal" in args[0] and "--tab" in command:
                # inject gnome-terminal environment variables
                if "GNOME_TERMINAL_SERVICE" not in env or "GNOME_TERMINAL_SCREEN" not in env:
                    env.update(self.gnome_terminal_env())
            process = subprocess.call(args, env=env)

        if sys.platform.startswith("win") and not hasattr(sys, '_called_from_test'):
            # bring the launched application to the front (Windows only)
            bring_window_to_front_from_pid(process.pid)

    def launch(self, command_line):
        """
        Launch a command

        :param command_line: command line to be launched
        """

        # replace the place-holders by the actual values
        command = command_line.replace("{host}", self._host)
        command = command.replace("{port}", str(self._port))
        command = command.replace("{url}", self._url)
        command = command.replace("{name}", self._params.get("name", "").replace('"', '\\"'))
        command = command.replace("{project}", self._params.get("project", "").replace('"', '\\"'))

        if "{display}" in command_line:
            if not self._url.startswith("gns3+vnc"):
                raise LauncherError("The {{display}} parameter is only supported for the gns3+vnc protocol scheme")
            else:
                command = command.replace("{display}", str(self._port - 5900))

        if "{pcap_file}" in command_line:
            raise LauncherError("The {{pcap_file}} parameter is only supported for the gns3+pcap protocol scheme")

        try:
            # replace the other params
            command = command.format(**self._params)
        except KeyError as e:
            raise LauncherError("{} could not be replaced in command '{}'".format(e, command))

        try:
            self._exec_command(command.strip())
        except (OSError, subprocess.SubprocessError) as e:
            raise LauncherError("Cannot start command  '{}': {}".format(command, e))


def launcher(argv):
    """
    Parse the URL and launch the command.
    """

    try:
        log.info('Parsing URL "{}"'.format(argv))
        url = urllib.parse.urlparse(argv)
        host = url.hostname
        if not host or host in ("0.0.0.0", "0:0:0:0:0:0:0:0", "::"):
            host = "localhost"

        url_data = {
            "url": url.geturl(),
            "host": host,
            "port": url.port or "",
            "path": url.path.lstrip("/") or "",
            "params": {}
        }
        if url.query:
            params = urllib.parse.parse_qs(url.query, keep_blank_values=True, strict_parsing=True)
            url_data["params"] = {k: v[0] for k, v in params.items()}
    except ValueError as e:
        raise LauncherError("Cannot parse URL '{}': {}".format(argv, e))

    local_config = LocalConfig.instance()
    command_settings = local_config.loadSectionSettings("CommandsSettings", COMMANDS_SETTINGS)
    if url.scheme == "gns3+telnet":
        command_line = command_settings["telnet_command"]
        log.info('Launching Telnet command: "{}"'.format(command_line))
    elif url.scheme == "gns3+vnc":
        if url.port and url.port < 5900:
            raise LauncherError("VNC requires a port superior or equal to 5900, current port is '{}'".format(url.port))
        command_line = command_settings["vnc_command"]
        log.info('Launching VNC command: "{}"'.format(command_line))
    elif url.scheme == "gns3+spice":
        command_line = command_settings["spice_command"]
        log.info('Launching SPICE command: "{}"'.format(command_line))
    elif url.scheme == "gns3+pcap":
        command_line = command_settings["pcap_command"]
        controller_settings = local_config.loadSectionSettings("ControllerSettings", CONTROLLER_SETTINGS)
        protocol = controller_settings["protocol"]
        accept_invalid_ssl_certificates = controller_settings["accept_invalid_ssl_certificates"]
        jwt_token = controller_settings["token"]
        user = controller_settings["username"]
        password = controller_settings["password"]
        log.info('Launching PCAP command: "{}"'.format(command_line))
        pcap_stream = PcapStream(command_line, protocol, user, password, jwt_token, accept_invalid_ssl_certificates, **url_data)
        pcap_stream.start()
        return
    else:
        raise LauncherError("Protocol not found or supported in URL '{}'".format(url.geturl()))

    if not command_line:
        raise LauncherError("No command configured for protocol handler '{}'".format(url.scheme))

    # launch the command
    command = Command(**url_data)
    command.launch(command_line)


def configure_logging(level):
    """
    Save logging info to a file.
    """

    logfile = os.path.join(LocalConfig.instance().configDirectory(), "launcher.log")
    logger = logging.getLogger()
    logger.setLevel(level)

    try:
        try:
            os.makedirs(os.path.dirname(logfile))
        except FileExistsError:
            pass
        stdout_handler = logging.StreamHandler(sys.stdout)
        logging.basicConfig(level=level, format="%(message)s", handlers=[stdout_handler])
        file_handler = logging.FileHandler(logfile, "w")
        file_handler.setLevel(level)
        logger.addHandler(file_handler)
    except OSError as e:
        log.warning("Cannot save log to {}: {}".format(logfile, e))


def main():
    """
    Entry point for GNS3 WebClient launcher
    """

    checks()
    configure_logging(logging.INFO)
    app = Application(sys.argv)

    if QtNetwork.QSslSocket.supportsSsl():
        log.info(f"SSL is supported, version: {QtNetwork.QSslSocket().sslLibraryBuildVersionString()}")

    try:
        import truststore
        truststore.inject_into_ssl()
        log.info("Using system certificate store for SSL connections")
    except ImportError:
        pass

    url_open_requests = []
    if sys.platform.startswith("darwin"):

        # intercept any QFileOpenEvent requests until the app is fully initialized.
        # NOTE: The QApplication must have the executable ($0) and filename
        # arguments passed in argv otherwise the FileOpen events are
        # triggered for them (this is done by Cocoa, but QApplication filters
        # them out if passed in argv)

        def on_request(url):
            url_open_requests.append(url)

        app.urlOpenedSignal.connect(on_request)
        app.processEvents()

        loop = QtCore.QEventLoop()
        app.urlOpenedSignal.connect(loop.quit)
        # wait 2 seconds to receive a URL open request
        QtCore.QTimer.singleShot(2000, loop.quit)

        if not loop.isRunning():
            loop.exec_()

        try:
            if not url_open_requests and hasattr(sys, "frozen"):
                # execute the WebClient configurator on macOS when there is QFileOpenEvent
                # since there can be only one main executable in an App.
                subprocess.Popen(["gns3-webclient-config"], env=os.environ)
                sys.exit(0)
        except (OSError, subprocess.SubprocessError) as e:
            QtWidgets.QMessageBox.critical(None, "GNS3 Command launcher {}".format(__version__), "Cannot start the WebClient config: {}".format(e))
            sys.exit(1)

    current_year = datetime.date.today().year
    log.info("GNS3 WebClient launcher version {}".format(__version__))
    log.info("Copyright (c) {} GNS3 Technologies Inc.".format(current_year))

    try:
        if url_open_requests:
            url = url_open_requests.pop()
        else:
            url = sys.argv[1]
        launcher(url)
    except IndexError:
        if hasattr(sys, "frozen"):
            program = sys.executable
        else:
            program = __file__
        QtWidgets.QMessageBox.critical(None, "GNS3 Command launcher {}".format(__version__), "usage: {} <url>".format(program))
        raise SystemExit("usage: {} <url>".format(program))
    except LauncherError as e:
        QtWidgets.QMessageBox.critical(None, "GNS3 Command launcher {}".format(__version__), "{}".format(e))
        log.critical("Could not launch using URL: {}".format(e))
        raise SystemExit("{}".format(e))


if __name__ == '__main__':
    main()
