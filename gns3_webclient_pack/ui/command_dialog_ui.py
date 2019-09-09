# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/grossmj/PycharmProjects/gns3-webclient-pack/gns3_webclient_pack/ui/command_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_uiCommandDialog(object):
    def setupUi(self, uiCommandDialog):
        uiCommandDialog.setObjectName("uiCommandDialog")
        uiCommandDialog.resize(685, 377)
        uiCommandDialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(uiCommandDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(uiCommandDialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.uiCommandComboBox = QtWidgets.QComboBox(uiCommandDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uiCommandComboBox.sizePolicy().hasHeightForWidth())
        self.uiCommandComboBox.setSizePolicy(sizePolicy)
        self.uiCommandComboBox.setObjectName("uiCommandComboBox")
        self.horizontalLayout.addWidget(self.uiCommandComboBox)
        self.uiRemovePushButton = QtWidgets.QPushButton(uiCommandDialog)
        self.uiRemovePushButton.setObjectName("uiRemovePushButton")
        self.horizontalLayout.addWidget(self.uiRemovePushButton)
        self.uiSavePushButton = QtWidgets.QPushButton(uiCommandDialog)
        self.uiSavePushButton.setObjectName("uiSavePushButton")
        self.horizontalLayout.addWidget(self.uiSavePushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label = QtWidgets.QLabel(uiCommandDialog)
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.uiCommandPlainTextEdit = QtWidgets.QPlainTextEdit(uiCommandDialog)
        self.uiCommandPlainTextEdit.setMinimumSize(QtCore.QSize(500, 0))
        self.uiCommandPlainTextEdit.setObjectName("uiCommandPlainTextEdit")
        self.verticalLayout.addWidget(self.uiCommandPlainTextEdit)
        self.uiButtonBox = QtWidgets.QDialogButtonBox(uiCommandDialog)
        self.uiButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.uiButtonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Help|QtWidgets.QDialogButtonBox.Ok)
        self.uiButtonBox.setObjectName("uiButtonBox")
        self.verticalLayout.addWidget(self.uiButtonBox)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(uiCommandDialog)
        self.uiButtonBox.accepted.connect(uiCommandDialog.accept)
        self.uiButtonBox.rejected.connect(uiCommandDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(uiCommandDialog)

    def retranslateUi(self, uiCommandDialog):
        _translate = QtCore.QCoreApplication.translate
        uiCommandDialog.setWindowTitle(_translate("uiCommandDialog", "Command"))
        self.label_2.setText(_translate("uiCommandDialog", "Choose a predefined command:"))
        self.uiRemovePushButton.setText(_translate("uiCommandDialog", "&Remove"))
        self.uiSavePushButton.setText(_translate("uiCommandDialog", "&Save"))
        self.label.setText(_translate("uiCommandDialog", "<html><head/><body><p>Or customize the current command:</p></body></html>"))
