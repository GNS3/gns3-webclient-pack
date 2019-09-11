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
import urllib.parse
import datetime

try:
    from gns3_webclient_pack.qt import QtGui, QtWidgets
except ImportError:
    raise SystemExit("Can't import Qt modules: Qt and/or PyQt is probably not installed correctly...")

from gns3_webclient_pack.main import main as configurator
from gns3_webclient_pack.local_config import LocalConfig
from gns3_webclient_pack.settings import COMMANDS_SETTINGS
from gns3_webclient_pack.version import __version__
from gns3_webclient_pack.utils.bring_to_front import bring_window_to_front_from_pid

import logging
log = logging.getLogger(__name__)


class LauncherError(Exception):

    def __init__(self, message):
        super().__init__(message)
        if isinstance(message, Exception):
            message = str(message)
        self._message = message

    def __repr__(self):
        return self._message

    def __str__(self):
        return self._message


class Command(object):

    def __init__(self, host, port, path, params, url):

        self._host = host
        self._port = port
        self._path = path
        self._params = params
        self._url = url

    def _exec_command(self, command):
        """
        Execute a command using subprocess

        :param command: command with all variables replaced
        """

        if sys.platform.startswith("win"):
            # use the string on Windows
            process = subprocess.Popen(command)
        else:
            # use arguments on other platforms
            try:
                args = shlex.split(command)
            except ValueError as e:
                raise LauncherError("Cannot parse '{}': {}".format(command, e))

            process = subprocess.Popen(args, env=os.environ)

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

        if "{display}" in command_line:
            if not self._url.startswith("gns3+vnc"):
                raise LauncherError("The {{display}} parameter is only supported for the gns3+vnc protocol scheme")
            else:
                command = command.replace("{display}", str(self._port - 5900))

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
        log.debug('Parsing URL "{}"'.format(argv))

        url = urllib.parse.urlparse(argv)
        url_data = {
            "url": url.geturl(),
            "host": url.hostname or "localhost",
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
    settings = local_config.loadSectionSettings("CommandsSettings", COMMANDS_SETTINGS)
    if url.scheme == "gns3+telnet":
        command_line = settings["telnet_command"]
        log.debug('Use telnet command: "{}"'.format(command_line))
    elif url.scheme == "gns3+vnc":
        if url.port and url.port < 5900:
            raise LauncherError("VNC requires a port superior or equal to 5900, current port is '{}'".format(url.port))
        command_line = settings["vnc_command"]
        log.debug('Use VNC command: "{}"'.format(command_line))
    elif url.scheme == "gns3+spice":
        command_line = settings["spice_command"]
        log.debug('Use SPICE command: "{}"'.format(command_line))
    else:
        raise LauncherError("Protocol not found or supported in URL '{}'".format(url.geturl()))

    if not command_line:
        raise LauncherError("No command configured for protocol handler '{}'".format(url.scheme))

    # launch the command
    command = Command(**url_data)
    command.launch(command_line)


def test(url):

    QtWidgets.QMessageBox.critical(None, "GNS3 Command launcher", "Launched with {}".format(url))


def main():
    """
    Entry point for GNS3 WebClient launcher
    """

    # Sometimes (for example at first launch) the OSX app service launcher add
    # an extra argument starting with -psn_. We filter it

    if sys.platform.startswith("darwin"):
        QtGui.QDesktopServices.setUrlHandler("gns3+telnet", test)
        sys.argv = [a for a in sys.argv if not a.startswith("-psn_")]
        if hasattr(sys, "frozen") and not sys.argv:
            # execute the WebClient configurator on macOS when there is no params
            # since there can be only one main executable in an App.
            configurator()
            sys.exit(0)

    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(":/images/gns3.ico"))
    current_year = datetime.date.today().year
    print("GNS3 WebClient launcher version {}".format(__version__))
    print("Copyright (c) {} GNS3 Technologies Inc.".format(current_year))

    try:
        print('Launching URL "{}"'.format(sys.argv[1]))
        launcher(sys.argv[1])
    except IndexError:
        if hasattr(sys, "frozen"):
            program = sys.executable
        else:
            program = __file__
        QtWidgets.QMessageBox.critical(None, "GNS3 Command launcher", "usage: {} <url>".format(program))
        raise SystemExit("usage: {} <url>".format(program))
    except LauncherError as e:
        QtWidgets.QMessageBox.critical(None, "GNS3 Command launcher", "{}".format(e))
        raise SystemExit("{}".format(e))


if __name__ == '__main__':
    main()
