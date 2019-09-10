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

import shlex
import pytest
from unittest.mock import patch
from gns3_webclient_pack.launcher import launcher, LauncherError
from gns3_webclient_pack.qt import QtWidgets


def test_telnet_command_on_linux(local_config):

    local_config.loadSectionSettings("CommandsSettings", {"telnet_command": "telnet {host} {port}"})
    with patch('subprocess.Popen') as popen, \
            patch('os.environ', new={}), \
            patch('sys.platform', new="linux"):
        launcher("gns3+telnet://localhost:6000")
        popen.assert_called_once_with(shlex.split("telnet localhost 6000"), env={})


def test_telnet_command_on_windows(local_config):

    local_config.loadSectionSettings("CommandsSettings", {"telnet_command": "telnet {host} {port}"})
    with patch('subprocess.Popen') as popen, \
            patch('sys.platform', new="win"):
        launcher("gns3+telnet://localhost:6000")
        popen.assert_called_once_with("telnet localhost 6000")


def test_telnet_command_no_port_on_windows(local_config):

    local_config.loadSectionSettings("CommandsSettings", {"telnet_command": "telnet {host} {port}"})
    with patch('subprocess.Popen') as popen, \
            patch('sys.platform', new="win"):
        launcher("gns3+telnet://localhost")
        popen.assert_called_once_with("telnet localhost")


def test_vnc_command_with_params(local_config):

    local_config.loadSectionSettings("CommandsSettings", {"vnc_command": "vncviewer {host} {port} {name} {project_id} {node_id} {display} {url}"})
    with patch('subprocess.Popen') as popen, \
            patch('os.environ', new={}), \
            patch('sys.platform', new="linux"):
        url = "gns3+vnc://localhost:5901?name=R1&project_id=1234&node_id=5678"
        launcher(url)
        popen.assert_called_once_with(shlex.split("vncviewer localhost 5901 R1 1234 5678 1 {}".format(url)), env={})


def test_vnc_command_with_invalid_port(qtbot, monkeypatch):

    monkeypatch.setattr(QtWidgets.QMessageBox, "critical", lambda *args: QtWidgets.QMessageBox.Ok)
    with pytest.raises(LauncherError):
        launcher("gns3+vnc://localhost:2000")


def test_telnet_command_with_non_ascii_characters(local_config):

    local_config.loadSectionSettings("CommandsSettings", {"telnet_command": "telnet {host} {port} {name}"})
    with patch('subprocess.Popen') as popen, \
            patch('sys.platform', new="win"):
        url = "gns3+telnet://localhost:6000?name=áÆÑß"
        launcher(url)
        popen.assert_called_once_with("telnet localhost 6000 áÆÑß")


def test_telnet_command_with_popen_issues(qtbot, monkeypatch):
    with patch('subprocess.Popen', side_effect=OSError("Dummy")):
        monkeypatch.setattr(QtWidgets.QMessageBox, "critical", lambda *args: QtWidgets.QMessageBox.Ok)
        with pytest.raises(LauncherError):
            launcher("gns3+telnet://localhost:6000")


def test_telnet_command_with_missing_scheme_in_url(qtbot, monkeypatch):

    monkeypatch.setattr(QtWidgets.QMessageBox, "critical", lambda *args: QtWidgets.QMessageBox.Ok)
    with pytest.raises(LauncherError):
        launcher("localhost:6000")


def test_telnet_command_with_incomplete_url(qtbot, monkeypatch):

    monkeypatch.setattr(QtWidgets.QMessageBox, "critical", lambda *args: QtWidgets.QMessageBox.Ok)
    with pytest.raises(LauncherError):
        launcher("gns3+telnet")


def test_telnet_command_with_port_out_of_range_in_url(qtbot, monkeypatch):
    monkeypatch.setattr(QtWidgets.QMessageBox, "critical", lambda *args: QtWidgets.QMessageBox.Ok)
    with pytest.raises(LauncherError):
        launcher("gns3+telnet://localhost:99999")


def test_vnc_command_on_linux(local_config):

    local_config.loadSectionSettings("CommandsSettings", {"vnc_command": "vncviewer {host} {port}"})
    with patch('subprocess.Popen') as popen, \
            patch('os.environ', new={}), \
            patch('sys.platform', new="linux"):
        launcher("gns3+vnc://localhost:6000")
        popen.assert_called_once_with(shlex.split("vncviewer localhost 6000"), env={})


def test_vnc_command_on_windows(local_config):

    local_config.loadSectionSettings("CommandsSettings", {"vnc_command": "vncviewer {host} {port}"})
    with patch('subprocess.Popen') as popen, \
            patch('sys.platform', new="win"):
        launcher("gns3+vnc://localhost:6000")
        popen.assert_called_once_with("vncviewer localhost 6000")


def test_spice_command_on_linux(local_config):

    local_config.loadSectionSettings("CommandsSettings", {"spice_command": "remote-viewer {host} {port}"})
    with patch('subprocess.Popen') as popen, \
            patch('os.environ', new={}), \
            patch('sys.platform', new="linux"):
        launcher("gns3+spice://localhost:6000")
        popen.assert_called_once_with(shlex.split("remote-viewer localhost 6000"), env={})


def test_spice_command_on_windows(local_config):

    local_config.loadSectionSettings("CommandsSettings", {"spice_command": "remote-viewer {host} {port}"})
    with patch('subprocess.Popen') as popen, \
            patch('sys.platform', new="win"):
        launcher("gns3+spice://localhost:6000")
        popen.assert_called_once_with("remote-viewer localhost 6000")
