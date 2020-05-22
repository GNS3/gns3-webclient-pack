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
import json
import base64
import subprocess
import shlex

from gns3_webclient_pack.qt import QtCore, QtWidgets, QtNetwork, qpartial, sip
from gns3_webclient_pack.version import __version__
from gns3_webclient_pack.launcher_error import LauncherError

import logging
log = logging.getLogger(__name__)


class PcapStream(QtCore.QObject):

    def __init__(self, command_line, host, port, path, params, url):

        super().__init__()
        self._network_manager = QtNetwork.QNetworkAccessManager()
        self._command_line = command_line
        self._host = host
        self._port = port
        self._path = path
        self._params = params
        self._url = url
        self._user = ""  #TODO: finish user authentication support
        self._password = ""
        self._capture_file = None
        self._loop = QtCore.QEventLoop()

    def _addAuth(self, request):
        """
        Adds basic authentication header
        """
        if self._user:
            auth_string = "{}:{}".format(self._user, self._password)
            auth_string = base64.b64encode(auth_string.encode("utf-8"))
            auth_string = "Basic {}".format(auth_string.decode())
            request.setRawHeader(b"Authorization", auth_string.encode())
        return request

    def _showError(self, error_message):

        QtWidgets.QMessageBox.critical(None, "GNS3 Command launcher", error_message)
        log.error(error_message)
        self._loop.quit()

    def start(self, timeout=30):
        """
        Start connection on PCAP stream and start the packet capture command.
        """

        if "project_id" not in self._params or "link_id" not in self._params:
            raise LauncherError("project_id and link_id are required URL parameters!")

        if self._user:
            QtCore.QUrl("http://{user}@{host}:{port}/v2/projects/{project_id}/links/{link_id}/pcap".format(user=self._user,
                                                                                                           host=self._host,
                                                                                                           port=self._port,
                                                                                                           project_id=self._params["project_id"],
                                                                                                           link_id=self._params["link_id"]))
        else:
            url = QtCore.QUrl("http://{host}:{port}/v2/projects/{project_id}/links/{link_id}/pcap".format(host=self._host,
                                                                                                          port=self._port,
                                                                                                          project_id=self._params["project_id"],
                                                                                                          link_id=self._params["link_id"]))
        request = QtNetwork.QNetworkRequest(url)
        request = self._addAuth(request)
        request.setRawHeader(b"User-Agent", "GNS3 WebClient pack v{version}".format(version=__version__).encode())

        try:
            response = self._network_manager.get(request)
        except SystemError as e:
            raise LauncherError("Error with network manager: {}".format(e))

        self._capture_file = QtCore.QTemporaryFile()
        self._capture_file.open(QtCore.QFile.WriteOnly)
        self._capture_file.setAutoRemove(True)
        self._startPacketCaptureCommand(self._capture_file.fileName())

        response.error.connect(qpartial(self._processError, response))
        response.readyRead.connect(qpartial(self._readPcapStreamCallback, response))
        response.finished.connect(self._loop.quit)
        response.error.connect(self._loop.quit)

        if timeout is not None:
           QtCore.QTimer.singleShot(timeout * 1000, qpartial(self._timeoutSlot, response, timeout))

        if not self._loop.isRunning():
            self._loop.exec_()

    def _processError(self, response, error_code):
        """
        Process error when reading PCAP stream.
        """

        if error_code != QtNetwork.QNetworkReply.NoError:
            error_message = response.errorString()

            if error_code < 200 or error_code == 403:
                if error_code == QtNetwork.QNetworkReply.OperationCanceledError:  # It's legit to cancel do not disconnect
                    error_message = "Operation timeout"  # It's clearer than cancel because cancel is triggered by us when we timeout
                elif error_code == QtNetwork.QNetworkReply.NetworkSessionFailedError:
                    # ignore the network session failed error to let the network manager recover from it
                    return
                return self._showError("Error while connecting to PCAP stream: {}".format(error_message))

            else:
                status = response.attribute(QtNetwork.QNetworkRequest.HttpStatusCodeAttribute)
                if status == 401:
                    return self._showError("Unauthorized request to PCAP stream: {}".format(error_message))

            try:
                body = bytes(response.readAll()).decode("utf-8").strip("\0")
                # Some time antivirus intercept our query and reply with garbage content
            except UnicodeError:
                body = None
            content_type = response.header(QtNetwork.QNetworkRequest.ContentTypeHeader)

            if body and content_type == "application/json":
                try:
                    return self._showError("Error from server while connecting to PCAP stream: {}".format(json.loads(body)["message"]))
                except (KeyError, ValueError):
                    # It happens when an antivirus catch the communication and send is error page without changing the Content Type
                    pass

            self._showError("Error when connecting to PCAP stream: {}".format(error_message))


    def _timeoutSlot(self, response, timeout):
        """
        Handle timed out request.
        """

        # We check if we received HTTP headers
        if not sip.isdeleted(response) and response.isRunning() and not len(response.rawHeaderList()) > 0:
            if not response.error() != QtNetwork.QNetworkReply.NoError:
                response.abort()
                raise LauncherError("Timeout after {} seconds for request {}".format(timeout, response.url().toString()))


    def _readPcapStreamCallback(self, response):
        """
        Process a packet received on the notification feed.
        """

        if response.error() != QtNetwork.QNetworkReply.NoError:
            return

        # HTTP error
        status = response.attribute(QtNetwork.QNetworkRequest.HttpStatusCodeAttribute)
        if status >= 300:
            return

        content_type = response.header(QtNetwork.QNetworkRequest.ContentTypeHeader)
        if content_type != "application/vnd.tcpdump.pcap":
            return

        content = bytes(response.readAll())
        self._capture_file.write(content)
        self._capture_file.flush()

    def _startPacketCaptureCommand(self, capture_file_path):
        """
        Starts the packet capture command.
        """

        command = self._command_line.replace("{pcap_file}", '"' + capture_file_path + '"')
        command = command.replace("{name}", self._params.get("name", "packet capture"))

        if "|" in command:
            # live traffic capture (using tail)
            command1, command2 = command.split("|", 1)
            info = None
            if sys.platform.startswith("win"):
                # hide tail window on Windows
                info = subprocess.STARTUPINFO()
                info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                info.wShowWindow = subprocess.SW_HIDE
                if hasattr(sys, "frozen"):
                    tail_path = os.path.dirname(os.path.abspath(sys.executable))  # for Popen to find tail.exe
                else:
                    # We suppose a developer will have tail the standard GNS3 location
                    tail_path = "C:\\Program Files\\GNS3"
                command1 = command1.replace("tail.exe", os.path.join(tail_path, "tail.exe"))
                command1 = command1.strip()
                command2 = command2.strip()
            else:
                try:
                    command1 = shlex.split(command1)
                    command2 = shlex.split(command2)
                except ValueError as e:
                    raise LauncherError("Invalid packet capture command {}: {}".format(command, e))
            try:
                tail_process = subprocess.Popen(command1, startupinfo=info, stdout=subprocess.PIPE)
                subprocess.Popen(command2, stdin=tail_process.stdout,stdout=subprocess.PIPE)
                tail_process.stdout.close()
            except OSError as e:
                raise LauncherError("Cannot start packet capture program {}".format(str(e)))
        else:
            # normal traffic capture
            if not sys.platform.startswith("win"):
                command = shlex.split(command)
            if len(command) == 0:
                raise LauncherError("No packet capture program configured")
            try:
                subprocess.Popen(command)
            except OSError as e:
                raise LauncherError("Can't start packet capture program {}".format(str(e)))
