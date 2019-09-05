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

from gns3_webclient_pack.local_config import LocalConfig
from gns3_webclient_pack.settings import COMMANDS_SETTINGS
from gns3_webclient_pack.version import __version__

import logging
log = logging.getLogger(__name__)


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
            subprocess.Popen(command)
        else:
            # use arguments on other platforms
            try:
                args = shlex.split(command)
            except ValueError as e:
                QtWidgets.QMessageBox.critical(None, "GNS3 Command launcher", "Cannot parse '{}': {}".format(command, e))
                sys.exit(1)
            subprocess.Popen(args, env=os.environ)

    def launch(self, command_line):
        """
        Launch a command

        :param command_line: command line to be launched
        """

        # replace the place-holders by the actual values
        command = command_line.replace("{host}", self._host)
        command = command.replace("{port}", self._port)
        command = command.replace("{url}", self._url)
        command = command.replace("{name}", self._params.get("name", "").replace('"', '\\"'))
        try:
            # replace the other params
            command = command.format(**self._params)
        except KeyError as e:
            QtWidgets.QMessageBox.critical(None, "GNS3 Command launcher", "{} could not be replaced in command '{}'".format(e, command))
            sys.exit(1)

        try:
            self._exec_command(command.strip())
        except (OSError, subprocess.SubprocessError) as e:
            QtWidgets.QMessageBox.critical(None, "GNS3 Command launcher", "Cannot start command  '{}': {}".format(command, e))
            sys.exit(1)


def main(argv):
    """
    Entry point for the command launcher.
    """

    try:
        log.debug('Parsing URL "{}"'.format(argv))
        url = urllib.parse.urlparse(argv)
        url_data = {
            "url": url.geturl(),
            "host": url.hostname or "localhost",
            "port": str(url.port) or "",
            "path": url.path.lstrip("/") or "",
            "params": {}
        }
        if url.query:
            params = urllib.parse.parse_qs(url.query, keep_blank_values=True, strict_parsing=True)
            url_data["params"] = {k: v[0] for k, v in params.items()}
    except ValueError as e:
        QtWidgets.QMessageBox.critical(None, "GNS3 Command launcher", "Cannot parse URL '{}': {}".format(url.geturl(), e))
        sys.exit(1)

    local_config = LocalConfig.instance()
    settings = local_config.loadSectionSettings("CommandsSettings", COMMANDS_SETTINGS)
    if url.scheme == "gns3+telnet":
        command_line = settings["telnet_command"]
        log.debug('Use telnet command: "{}"'.format(command_line))
        command = Command(**url_data)
        command.launch(command_line)
    elif url.scheme == "gns3+vnc":
        command_line = settings["vnc_command"]
        log.debug('Use VNC command: "{}"'.format(command_line))
        raise NotImplementedError
    elif url.scheme == "gns3+spice":
        command_line = settings["spice_command"]
        log.debug('Use SPICE command: "{}"'.format(command_line))
        raise NotImplementedError
    else:
        QtWidgets.QMessageBox.critical(None, "GNS3 Command launcher", "Protocol not found or supported in URL '{}'".format(url.geturl()))
        sys.exit(1)


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(":/images/gns3.ico"))
    current_year = datetime.date.today().year
    #logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(levelname)s %(filename)s %(lineno)s - %(message)s")
    print("GNS3 WebClient pack version {}".format(__version__))
    print("Copyright (c) {} GNS3 Technologies Inc.".format(current_year))
    try:
        main(sys.argv[1])
    except IndexError:
        if hasattr(sys, "frozen"):
            program = sys.executable
        else:
            program = __file__
        print("usage: {}".format(program), "<url>", file=sys.stderr)
        sys.exit(1)
