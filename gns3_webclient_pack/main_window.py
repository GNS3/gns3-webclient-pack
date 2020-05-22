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

"""
Main window for the WebClient pack.
"""

import logging

from .local_config import LocalConfig
from .qt import QtGui, QtCore, QtWidgets
from .ui.main_window_ui import Ui_MainWindow
from .dialogs.about_dialog import AboutDialog
from .dialogs.command_dialog import CommandDialog
from .settings import (GENERAL_SETTINGS, COMMANDS_SETTINGS)

log = logging.getLogger(__name__)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    Main window implementation.

    :param parent: parent widget
    """

    def __init__(self, parent=None):

        super().__init__(parent)
        self._settings = {}
        self._commands_settings = {}
        self.setupUi(self)
        self.resize(self.width(), self.minimumHeight())

        MainWindow._instance = self
        self._local_config = LocalConfig.instance()
        self._loadSettings()
        self._commands_saved = True

        # restore the geometry and state of the main window.
        self.restoreGeometry(QtCore.QByteArray().fromBase64(self._settings["geometry"].encode()))
        self.restoreState(QtCore.QByteArray().fromBase64(self._settings["state"].encode()))

        # load initial stuff once the event loop isn't busy
        QtCore.QTimer.singleShot(0, self._startupLoading)

        # help menu connections
        self.uiOnlineHelpAction.triggered.connect(self._onlineHelpActionSlot)
        self.uiAboutQtAction.triggered.connect(self._aboutQtActionSlot)
        self.uiAboutAction.triggered.connect(self._aboutActionSlot)

        # button connections
        self.uiTelnetCommandPushButton.clicked.connect(self._telnetCommandSlot)
        self.uiVNCCommandPushButton.clicked.connect(self._vncCommandSlot)
        self.uiSPICECommandPushButton.clicked.connect(self._spiceCommandSlot)
        self.uiPacketCaptureCommandPushButton.clicked.connect(self._packetCaptureCommandSlot)

        self.uiButtonBox.button(QtWidgets.QDialogButtonBox.Close).clicked.connect(self.close)
        self.uiButtonBox.button(QtWidgets.QDialogButtonBox.Apply).clicked.connect(self._applySlot)
        self.uiButtonBox.button(QtWidgets.QDialogButtonBox.Reset).clicked.connect(self._resetSlot)

        # custom button icons
        self.uiButtonBox.button(QtWidgets.QDialogButtonBox.Reset).setIcon(QtGui.QIcon(":/icons/reload.svg"))

    def _loadSettings(self):
        """
        Loads the settings from the persistent settings file.
        """

        self._settings = self._local_config.loadSectionSettings("GeneralSettings", GENERAL_SETTINGS)
        self._commands_settings = self._local_config.loadSectionSettings("CommandsSettings", COMMANDS_SETTINGS)
        self.uiTelnetCommandLineEdit.setText(self._commands_settings["telnet_command"])
        self.uiVNCCommandLineEdit.setText(self._commands_settings["vnc_command"])
        self.uiSPICECommandLineEdit.setText(self._commands_settings["spice_command"])
        self.uiPacketCaptureCommandLineEdit.setText(self._commands_settings["pcap_command"])
        self.uiPacketCaptureCommandLineEdit.textChanged.connect(self._commandChangedSlot)
        self.uiTelnetCommandLineEdit.textChanged.connect(self._commandChangedSlot)
        self.uiVNCCommandLineEdit.textChanged.connect(self._commandChangedSlot)
        self.uiSPICECommandLineEdit.textChanged.connect(self._commandChangedSlot)

    def settings(self):
        """
        Returns the general settings.

        :returns: settings dictionary
        """

        return self._settings

    def setSettings(self, new_settings):
        """
        Set new general settings.

        :param new_settings: settings dictionary
        """

        self._settings.update(new_settings)
        # save the settings
        LocalConfig.instance().saveSectionSettings("GeneralSettings", self._settings)

    def _onlineHelpActionSlot(self):
        """
        Slot to launch a browser pointing to the documentation page.
        """

        QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://docs.gns3.com/"))

    def _aboutQtActionSlot(self):
        """
        Slot to display the Qt About dialog.
        """

        QtWidgets.QMessageBox.aboutQt(self)

    def _aboutActionSlot(self):
        """
        Slot to display the GNS3 About dialog.
        """

        dialog = AboutDialog(self)
        dialog.show()
        dialog.exec_()

    def _commandChangedSlot(self):
        """
        Slot to detect changes to commands.
        """

        self._commands_saved = False

    def _telnetCommandSlot(self):
        """
        Slot to set a chosen Telnet command.
        """

        cmd = self.uiTelnetCommandLineEdit.text()
        (ok, cmd) = CommandDialog.getCommand(self, console_type="telnet", current=cmd)
        if ok:
            self.uiTelnetCommandLineEdit.setText(cmd)

    def _vncCommandSlot(self):
        """
        Slot to set a chosen VNC command.
        """

        cmd = self.uiVNCCommandLineEdit.text()
        (ok, cmd) = CommandDialog.getCommand(self, console_type="vnc", current=cmd)
        if ok:
            self.uiVNCCommandLineEdit.setText(cmd)

    def _spiceCommandSlot(self):
        """
        Slot to set a chosen SPICE command.
        """

        cmd = self.uiSPICECommandLineEdit.text()
        (ok, cmd) = CommandDialog.getCommand(self, console_type="spice", current=cmd)
        if ok:
            self.uiSPICECommandLineEdit.setText(cmd)

    def _packetCaptureCommandSlot(self):
        """
        Slot to set a chosen packet capture command.
        """

        cmd = self.uiPacketCaptureCommandLineEdit.text()
        (cmd, ok) = QtWidgets.QInputDialog.getText(self, "Command", "Packet capture command", text=cmd)
        if ok:
            self.uiPacketCaptureCommandLineEdit.setText(cmd)

    def _applySlot(self):
        """
        Save the commands in the settings file.
        """

        self._commands_settings["telnet_command"] = self.uiTelnetCommandLineEdit.text().strip()
        self._commands_settings["vnc_command"] = self.uiVNCCommandLineEdit.text().strip()
        self._commands_settings["spice_command"] = self.uiSPICECommandLineEdit.text().strip()
        self._commands_settings["pcap_command"] = self.uiPacketCaptureCommandLineEdit.text().strip()
        LocalConfig.instance().saveSectionSettings("CommandsSettings", self._commands_settings)
        self.setSettings(self._settings)
        self._commands_saved = True

    def _resetSlot(self):
        """
        Reset the commands to their default value.
        """

        self.uiTelnetCommandLineEdit.setText(COMMANDS_SETTINGS["telnet_command"])
        self.uiVNCCommandLineEdit.setText(COMMANDS_SETTINGS["vnc_command"])
        self.uiSPICECommandLineEdit.setText(COMMANDS_SETTINGS["spice_command"])
        self.uiPacketCaptureCommandLineEdit.setText(COMMANDS_SETTINGS["pcap_command"])

    def closeEvent(self, event):
        """
        Handles the event when the main window is closed.

        :param event: QCloseEvent
        """

        if self._commands_saved is False:
            reply = QtWidgets.QMessageBox.question(self, "Unsaved changes", "Save changes before closing?",
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel)
            if reply == QtWidgets.QMessageBox.Yes:
                self._applySlot()
            elif reply == QtWidgets.QMessageBox.Cancel:
                event.ignore()
                return

        self._settings["geometry"] = bytes(self.saveGeometry().toBase64()).decode()
        self._settings["state"] = bytes(self.saveState().toBase64()).decode()
        self.setSettings(self._settings)
        self.close()
        event.accept()

    def _startupLoading(self):
        """
        Called by QTimer.singleShot to load everything needed at startup.
        """

        pass

    @staticmethod
    def instance():
        """
        Singleton to return only one instance of MainWindow.

        :returns: instance of MainWindow
        """

        if not hasattr(MainWindow, "_instance"):
            MainWindow._instance = MainWindow()
        return MainWindow._instance
