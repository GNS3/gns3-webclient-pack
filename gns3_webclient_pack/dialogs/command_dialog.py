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

import copy

from gns3_webclient_pack.qt import QtGui, QtWidgets
from gns3_webclient_pack.local_config import LocalConfig
from gns3_webclient_pack.ui.command_dialog_ui import Ui_uiCommandDialog
from gns3_webclient_pack.settings import (PRECONFIGURED_TELNET_COMMANDS,
                                          PRECONFIGURED_VNC_COMMANDS,
                                          PRECONFIGURED_SPICE_COMMANDS,
                                          CUSTOM_COMMANDS_SETTINGS)

import logging
log = logging.getLogger(__name__)


class CommandDialog(QtWidgets.QDialog, Ui_uiCommandDialog):
    """
    This dialog allow user to select the command used to start a
    console.
    """

    def __init__(self, parent, console_type="telnet", current=None):
        """
        :params console_type: telnet, serial, vnc or spice
        :params current: Current console command
        """
        super().__init__(parent)
        self.setupUi(self)
        self.resize(self.width(), self.minimumHeight())

        self._console_type = console_type
        self._current = current
        self._settings = LocalConfig.instance().loadSectionSettings("CustomCommands", CUSTOM_COMMANDS_SETTINGS)

        self.uiCommandComboBox.currentIndexChanged.connect(self.commandComboBoxCurrentIndexChangedSlot)
        self.uiCommandPlainTextEdit.textChanged.connect(self.textChangedSlot)
        self.uiSavePushButton.clicked.connect(self._savePushButtonClickedSlot)
        self.uiRemovePushButton.clicked.connect(self._removePushButtonClickedSlot)
        self.uiButtonBox.button(QtWidgets.QDialogButtonBox.Help).clicked.connect(self._helpSlot)

        # custom button icons
        self.uiButtonBox.button(QtWidgets.QDialogButtonBox.Help).setIcon(QtGui.QIcon(":/icons/help.svg"))

        self._refreshList()

    def _refreshList(self):

        if self._console_type == "telnet":
            self._consoles = copy.copy(PRECONFIGURED_TELNET_COMMANDS)
            self._consoles.update(self._settings[self._console_type])
        elif self._console_type == "vnc":
            self._consoles = copy.copy(PRECONFIGURED_VNC_COMMANDS)
            self._consoles.update(self._settings[self._console_type])
        elif self._console_type.startswith("spice"):
            self._consoles = copy.copy(PRECONFIGURED_SPICE_COMMANDS)
            self._consoles.update(self._settings[self._console_type])

        self.uiCommandComboBox.clear()
        self.uiCommandComboBox.addItem("Custom", "")
        for name, cmd in sorted(self._consoles.items(), key=(lambda item: item[0].lower())):
            self.uiCommandComboBox.addItem(name, cmd)

        if self._current:
            self.uiCommandPlainTextEdit.setPlainText(self._current)
        else:
            self.uiCommandComboBox.setCurrentIndex(1)

    def _helpSlot(self):
        """
        Shows the help for this dialog
        """

        help_text = """The following variables will be replaced before executing a command:

{host}: IP address or hostname
{port}: port number
{display}: VNC display
{name}: device name
{project_id}: project UUID
{node_id}: node UUID
{url}: server URL (http://user:password@server:port)
    """
        QtWidgets.QMessageBox.information(self, "Help for command variables", help_text)

    def _removePushButtonClickedSlot(self):
        """
        Remove the custom command from the custom list
        """

        self._settings[self._console_type].pop(self.uiCommandComboBox.currentText())
        LocalConfig.instance().saveSectionSettings("CustomCommands", self._settings)
        self._current = None
        self._refreshList()

    def _savePushButtonClickedSlot(self):
        """
        Save a custom command to the list
        """

        name, ok = QtWidgets.QInputDialog.getText(self, "Add a command", "Command name:", QtWidgets.QLineEdit.Normal)
        command = self.uiCommandPlainTextEdit.toPlainText().strip()
        if ok and len(command) > 0:
            if command not in self._consoles.values():
                self._settings[self._console_type][name] = command
                self._current = command
                LocalConfig.instance().saveSectionSettings("CustomCommands", self._settings)
                self._refreshList()

    def textChangedSlot(self):
        index = self.uiCommandComboBox.findData(self.uiCommandPlainTextEdit.toPlainText())
        if index == -1:
            index = 0
        self.uiCommandComboBox.setCurrentIndex(index)

    def commandComboBoxCurrentIndexChangedSlot(self, index):
        self.uiRemovePushButton.hide()
        # Ignore custom command
        if index != 0:
            self.uiCommandPlainTextEdit.setPlainText(self.uiCommandComboBox.currentData())
            self.uiSavePushButton.hide()
            if self.uiCommandComboBox.currentText() in self._settings[self._console_type].keys():
                self.uiRemovePushButton.show()
        else:
            self.uiSavePushButton.show()

    @staticmethod
    def getCommand(parent, console_type="telnet", current=None):
        dialog = CommandDialog(parent, console_type=console_type, current=current)
        dialog.show()
        if dialog.exec_():
            return True, dialog.uiCommandPlainTextEdit.toPlainText().replace("\n", " ")
        return False, None


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main = QtWidgets.QMainWindow()
    (ok, command) = CommandDialog.getCommand(main, console_type="telnet", current=list(PRECONFIGURED_TELNET_COMMANDS.items())[0][1])
    print(ok)
    print(command)

