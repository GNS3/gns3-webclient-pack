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

from ..qt import QtWidgets
from ..version import __version__
from ..ui.about_dialog_ui import Ui_AboutDialog


class AboutDialog(QtWidgets.QDialog, Ui_AboutDialog):
    """
    About dialog.
    """

    def __init__(self, parent):

        super().__init__(parent)
        self.setupUi(self)
        self.adjustSize()

        # dynamically add the current version number
        text = self.uiAboutTextLabel.text()
        text = text.replace("%VERSION%", __version__)
        self.uiAboutTextLabel.setText(text)
