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
from typing import List, Optional

from gns3_webclient_pack.dialogs.login_dialog import LoginDialog
from gns3_webclient_pack.local_config import LocalConfig
from gns3_webclient_pack.settings import CONTROLLER_SETTINGS
from gns3_webclient_pack.qt import QtCore, QtWidgets, QtNetwork, qpartial, sip
from gns3_webclient_pack.version import __version__
from gns3_webclient_pack.launcher_error import LauncherError


import logging
log = logging.getLogger(__name__)


class QNetworkReplyWatcher(QtCore.QObject):
    """
    Synchronously wait for a QNetworkReply to be completed
    """

    def __init__(self, parent: QtWidgets.QWidget = None):

        super().__init__(parent)

    def waitForReply(self, reply: QtNetwork.QNetworkReply, timeout=60) -> None:
        """
        Wait for the QNetworkReply to be complete or for the timeout

        :param reply: QNetworkReply instance
        :param timeout: Number of seconds before timeout
        """

        loop = QtCore.QEventLoop()

        if timeout:
            timer = QtCore.QTimer(self)
            timer.setSingleShot(True)
            timer.timeout.connect(lambda: loop.exit(1))
            timer.start(timeout * 1000)

        reply.finished.connect(loop.quit)

        if not loop.isRunning():
            if loop.exec_() == 1:
                raise LauncherError(f"Request to '{reply.url().toString()}' timed out after {timeout} seconds")

        if timeout and timer.isActive():
            timer.stop()

class PcapStream(QtCore.QObject):

    def __init__(self, command_line, protocol, user, password, jwt_token, accept_invalid_ssl_certificates, host, port, path, params, url):

        super().__init__()
        self._network_manager = QtNetwork.QNetworkAccessManager()
        self._command_line = command_line
        self._protocol = protocol
        self._accept_invalid_ssl_certificates = accept_invalid_ssl_certificates
        self._api_version = "v2"
        self._host = host
        self._port = port
        self._path = path
        self._params = params
        self._url = url
        self._user = user
        self._password = password
        self._capture_file = None
        self._jwt_token = jwt_token
        self._auth_attempted = False
        self._loop = QtCore.QEventLoop()

        self._network_manager.sslErrors.connect(self._handleSSLErrorsSlot)
        # Store SSL error exceptions
        self._ssl_exceptions = {}

    def _addBasicAuth(self, request: QtNetwork.QNetworkRequest) -> QtNetwork.QNetworkRequest:
        """
        Adds basic authentication header
        """
        if self._user:
            auth_string = "{}:{}".format(self._user, self._password)
            auth_string = base64.b64encode(auth_string.encode("utf-8"))
            auth_string = "Basic {}".format(auth_string.decode())
            request.setRawHeader(b"Authorization", auth_string.encode())
        return request

    def _addBearerAuth(self, request: QtNetwork.QNetworkRequest) -> QtNetwork.QNetworkRequest:
        """
        Add the JWT token in the authentication header
        """

        if self._jwt_token:
            request.setRawHeader(b"Authorization", f"Bearer {self._jwt_token}".encode())
        return request

    def _showError(self, error_message: str) -> None:

        QtWidgets.QMessageBox.critical(None, "GNS3 Command launcher {}".format(__version__), error_message)
        log.error(error_message)
        self._loop.quit()

    def start(self, timeout: int = 30) -> None:
        """
        Start connection on PCAP stream and start the packet capture command.
        """

        if "project_id" not in self._params or "link_id" not in self._params:
            raise LauncherError("project_id and link_id are required URL parameters!")

        if "protocol" in self._params and self._params["protocol"]:
            protocol = self._params["protocol"]
            if self._protocol != protocol:
                log.warning("Protocol mismatch between URL and controller settings: {} != {}".format(self._protocol, protocol))
            self._protocol = protocol

        if self._protocol == "https" and not QtNetwork.QSslSocket.supportsSsl():
            raise LauncherError("SSL is not supported")

        try:
            self._executeHTTPQuery("GET", "/version", wait=True)
            log.info("API version 2 detected")
            endpoint = "pcap"
        except LauncherError:
            log.info("API version 3 detected")
            self._api_version = "v3"
            self._executeHTTPQuery("GET", "/access/users/me", wait=True)  # check if we are authenticated
            endpoint = "capture/stream"  # pcap endpoint was renamed in v3

        url = QtCore.QUrl(
            "{protocol}://{host}:{port}/{api_version}/projects/{project_id}/links/{link_id}/{endpoint}".format(
                protocol=self._protocol,
                host=self._host,
                port=self._port,
                api_version=self._api_version,
                project_id=self._params["project_id"],
                link_id=self._params["link_id"],
                endpoint=endpoint)
        )

        request = QtNetwork.QNetworkRequest(url)
        if self._api_version == "v2":
            # v2 of the API has basic HTTP authentication
            self._addBasicAuth(request)
        else:
            self._addBearerAuth(request)

        request.setRawHeader(b"User-Agent", "GNS3 WebClient pack v{version}".format(version=__version__).encode())
        try:
            response = self._network_manager.get(request)
        except SystemError as e:
            raise LauncherError("Error with network manager: {}".format(e))

        self._capture_file = QtCore.QTemporaryFile()
        self._capture_file.open(QtCore.QFile.WriteOnly)
        self._capture_file.setAutoRemove(True)
        process = self._startPacketCaptureCommand(self._capture_file.fileName())

        response.error.connect(qpartial(self._processError, response))
        response.readyRead.connect(qpartial(self._readPcapStreamCallback, response))
        response.finished.connect(self._loop.quit)
        response.finished.connect(process.kill)
        response.error.connect(self._loop.quit)

        if timeout is not None:
           QtCore.QTimer.singleShot(timeout * 1000, qpartial(self._timeoutSlot, response, timeout))

        if not self._loop.isRunning():
            self._loop.exec_()

    def _processError(self, response: QtNetwork.QNetworkReply, error_code: int) -> None:
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
                    return self._showError("Error from server while connected to PCAP stream: {}".format(json.loads(body)["message"]))
                except (KeyError, ValueError):
                    # It happens when an antivirus catch the communication and send is error page without changing the Content Type
                    pass

            self._showError("Error when connecting to PCAP stream: {}".format(error_message))

    def _requestCredentialsFromUser(self):
        """
        Request credentials from user

        :return: username, password
        """

        username = password = None
        login_dialog = LoginDialog(None)
        if self._user:
            login_dialog.setUsername(self._user)
        login_dialog.show()
        login_dialog.raise_()
        if login_dialog.exec_():
            username = login_dialog.getUsername()
            password = login_dialog.getPassword()
        return username, password

    def _handleUnauthorizedRequest(self, reply: QtNetwork.QNetworkReply) -> None:
        """
        Request the username / password to authenticate with the server
        """

        if not self._user or not self._password or self._auth_attempted is True:
            username, password = self._requestCredentialsFromUser()
        else:
            username = self._user
            password = self._password

        if username and password:
            body = {
                "username": username,
                "password": password
            }
            self._auth_attempted = True
            content = self._executeHTTPQuery("POST", "/access/users/authenticate", body=body, wait=True)
            if content:
                log.info(f"Authenticated with controller {self._host} on port {self._port}")
                token = content.get("access_token")
                if token:
                    self._auth_attempted = False
                    self._jwt_token = token
                    # save the token for future sessions
                    controller_settings = LocalConfig.instance().loadSectionSettings("ControllerSettings", CONTROLLER_SETTINGS)
                    controller_settings["token"] = token
                    LocalConfig.instance().saveSectionSettings("ControllerSettings", controller_settings)
                    return
        else:
            self._jwt_token = None
            raise LauncherError(f"{reply.errorString()}")


    def _executeHTTPQuery(
            self,
            method: str,
            endpoint: str,
            body: dict = None,
            timeout: int = 60,
            wait: bool = False,

    ) -> Optional[str]:
        """
        Send an HTTP request

        :param method: HTTP method
        :param endpoint: API endpoint
        :param body: Body to send (dictionary, string or pathlib.Path)
        :param timeout: Delay in seconds before raising a timeout
        :param params: Query parameters
        :param wait: Wait for server reply asynchronously
        """

        url = QtCore.QUrl(
            "{protocol}://{host}:{port}/{api_version}{endpoint}".format(
                protocol=self._protocol,
                host=self._host,
                port=self._port,
                api_version=self._api_version,
                endpoint=endpoint)
        )

        request = QtNetwork.QNetworkRequest(QtCore.QUrl(url))
        if self._api_version == "v2":
            self._addBasicAuth(request)
        else:
            self._addBearerAuth(request)

        request.setRawHeader(b"User-Agent", "GNS3 WebClient pack v{version}".format(version=__version__).encode())
        body = self._addBodyToRequest(body, request)

        try:
            response = self._network_manager.sendCustomRequest(request, method.encode(), body)
        except SystemError as e:
            raise LauncherError("Error with network manager: {}".format(e))

        if wait:
            QNetworkReplyWatcher().waitForReply(response, timeout)
            if response.error() == QtNetwork.QNetworkReply.NoError:
                content_type = response.header(QtNetwork.QNetworkRequest.ContentTypeHeader)
                try:
                    content = bytes(response.readAll())
                    content = content.decode("utf-8").strip(" \0\n\t")
                    if content and content_type == "application/json":
                        content = json.loads(content)
                    return content
                except ValueError as e:
                    raise LauncherError(f"Could not read data with content type '{content_type}' returned from"
                        f" '{response.url().toString()}': {e}")
            else:
                status = response.attribute(QtNetwork.QNetworkRequest.HttpStatusCodeAttribute)
                if status == 401 and response.rawHeader(b"WWW-Authenticate") == b"Bearer":
                    self._handleUnauthorizedRequest(response)
                else:
                    raise LauncherError(f"{response.errorString()}")


    def _addBodyToRequest(
            self,
            body: dict,
            request: QtNetwork.QNetworkRequest
    ) -> Optional[QtCore.QBuffer]:
        """
        Add the required headers for sending the body.

        :param body: body to send in request
        :returns: body compatible with Qt
        """

        if body is None:
            return None

        if isinstance(body, dict):
            body = json.dumps(body)
            data = QtCore.QByteArray(body.encode())
            body = QtCore.QBuffer(self)
            body.setData(data)
            body.open(QtCore.QIODevice.ReadOnly)
            request.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader, "application/json")
            request.setHeader(QtNetwork.QNetworkRequest.ContentLengthHeader, str(data.size()))
            return body


    def _timeoutSlot(self, response: QtNetwork.QNetworkReply, timeout: int) -> None:
        """
        Handle timed out request.
        """

        # We check if we received HTTP headers
        if not sip.isdeleted(response) and response.isRunning() and not len(response.rawHeaderList()) > 0:
            if not response.error() != QtNetwork.QNetworkReply.NoError:
                response.abort()
                raise LauncherError("Timeout after {} seconds for request {}".format(timeout, response.url().toString()))


    def _readPcapStreamCallback(self, response: QtNetwork.QNetworkReply) -> None:
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

    def _startPacketCaptureCommand(self, capture_file_path: str) -> subprocess.Popen:
        """
        Starts the packet capture command.
        """

        command = self._command_line.replace("{pcap_file}", '"' + capture_file_path + '"')
        command = command.replace("{name}", self._params.get("name", "unknown packet capture"))
        command = command.replace("{project}", self._params.get("project", "unknown project"))

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
                return tail_process
            except OSError as e:
                raise LauncherError("Cannot start packet capture program {}".format(str(e)))
        else:
            # normal traffic capture
            if not sys.platform.startswith("win"):
                command = shlex.split(command)
            if len(command) == 0:
                raise LauncherError("No packet capture program configured")
            try:
                process = subprocess.Popen(command)
            except OSError as e:
                raise LauncherError("Can't start packet capture program {}".format(str(e)))
            return process

    def _handleSSLErrorsSlot(self, reply: QtNetwork.QNetworkReply, ssl_errors: List[QtNetwork.QSslError]) -> None:
        """
        Handle SSL errors
        """

        if self._accept_invalid_ssl_certificates:
            reply.ignoreSslErrors()
            return

        url = reply.request().url()
        host_port_key = f"{url.host()}:{url.port()}"

        # get the certificate digest
        ssl_config = reply.sslConfiguration()
        peer_cert = ssl_config.peerCertificate()
        digest = peer_cert.digest()

        if host_port_key in self._ssl_exceptions:
            if self._ssl_exceptions[host_port_key] == digest:
                reply.ignoreSslErrors()
                return

        msgbox = QtWidgets.QMessageBox(None)
        msgbox.setWindowTitle("SSL error detected")
        msgbox.setText(f"This server could not prove that it is {url.host()}:{url.port()}. Please carefully examine the certificate to make sure the server can be trusted.")
        msgbox.setInformativeText(f"{ssl_errors[0].errorString()}")
        msgbox.setDetailedText(peer_cert.toText())
        msgbox.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        connect_button = QtWidgets.QPushButton(f"&Connect to {url.host()}:{url.port()}", msgbox)
        msgbox.addButton(connect_button, QtWidgets.QMessageBox.YesRole)
        abort_button = QtWidgets.QPushButton("&Abort", msgbox)
        msgbox.addButton(abort_button, QtWidgets.QMessageBox.RejectRole)
        msgbox.setDefaultButton(abort_button)
        msgbox.setIcon(QtWidgets.QMessageBox.Critical)
        msgbox.exec_()

        if msgbox.clickedButton() == connect_button:
            self._ssl_exceptions[host_port_key] = digest
            reply.ignoreSslErrors()
        else:
            for error in ssl_errors:
                log.error(f"SSL error detected: {error.errorString()}")
