# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/grossmj/PycharmProjects/gns3-webclient-pack/gns3_webclient_pack/ui/main_window.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        self.uiCentralWidget = QtWidgets.QWidget(MainWindow)
        self.uiCentralWidget.setObjectName("uiCentralWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.uiCentralWidget)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 7, 0, 1, 1)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.uiTelnetCommandLineEdit = QtWidgets.QLineEdit(self.uiCentralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uiTelnetCommandLineEdit.sizePolicy().hasHeightForWidth())
        self.uiTelnetCommandLineEdit.setSizePolicy(sizePolicy)
        self.uiTelnetCommandLineEdit.setReadOnly(True)
        self.uiTelnetCommandLineEdit.setObjectName("uiTelnetCommandLineEdit")
        self.horizontalLayout_9.addWidget(self.uiTelnetCommandLineEdit)
        self.uiTelnetCommandPushButton = QtWidgets.QPushButton(self.uiCentralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uiTelnetCommandPushButton.sizePolicy().hasHeightForWidth())
        self.uiTelnetCommandPushButton.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/config.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.uiTelnetCommandPushButton.setIcon(icon)
        self.uiTelnetCommandPushButton.setIconSize(QtCore.QSize(16, 16))
        self.uiTelnetCommandPushButton.setObjectName("uiTelnetCommandPushButton")
        self.horizontalLayout_9.addWidget(self.uiTelnetCommandPushButton)
        self.gridLayout.addLayout(self.horizontalLayout_9, 1, 0, 1, 1)
        self.uiVNCCommandLabel = QtWidgets.QLabel(self.uiCentralWidget)
        self.uiVNCCommandLabel.setObjectName("uiVNCCommandLabel")
        self.gridLayout.addWidget(self.uiVNCCommandLabel, 2, 0, 1, 1)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.uiVNCCommandLineEdit = QtWidgets.QLineEdit(self.uiCentralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uiVNCCommandLineEdit.sizePolicy().hasHeightForWidth())
        self.uiVNCCommandLineEdit.setSizePolicy(sizePolicy)
        self.uiVNCCommandLineEdit.setText("")
        self.uiVNCCommandLineEdit.setReadOnly(True)
        self.uiVNCCommandLineEdit.setObjectName("uiVNCCommandLineEdit")
        self.horizontalLayout_8.addWidget(self.uiVNCCommandLineEdit)
        self.uiVNCCommandPushButton = QtWidgets.QPushButton(self.uiCentralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uiVNCCommandPushButton.sizePolicy().hasHeightForWidth())
        self.uiVNCCommandPushButton.setSizePolicy(sizePolicy)
        self.uiVNCCommandPushButton.setIcon(icon)
        self.uiVNCCommandPushButton.setObjectName("uiVNCCommandPushButton")
        self.horizontalLayout_8.addWidget(self.uiVNCCommandPushButton)
        self.gridLayout.addLayout(self.horizontalLayout_8, 3, 0, 1, 1)
        self.uiSPICECommandLabel = QtWidgets.QLabel(self.uiCentralWidget)
        self.uiSPICECommandLabel.setObjectName("uiSPICECommandLabel")
        self.gridLayout.addWidget(self.uiSPICECommandLabel, 4, 0, 1, 1)
        self.uiTelnetCommandLabel = QtWidgets.QLabel(self.uiCentralWidget)
        self.uiTelnetCommandLabel.setObjectName("uiTelnetCommandLabel")
        self.gridLayout.addWidget(self.uiTelnetCommandLabel, 0, 0, 1, 1)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.uiSPICECommandLineEdit = QtWidgets.QLineEdit(self.uiCentralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uiSPICECommandLineEdit.sizePolicy().hasHeightForWidth())
        self.uiSPICECommandLineEdit.setSizePolicy(sizePolicy)
        self.uiSPICECommandLineEdit.setText("")
        self.uiSPICECommandLineEdit.setReadOnly(True)
        self.uiSPICECommandLineEdit.setObjectName("uiSPICECommandLineEdit")
        self.horizontalLayout_10.addWidget(self.uiSPICECommandLineEdit)
        self.uiSPICECommandPushButton = QtWidgets.QPushButton(self.uiCentralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uiSPICECommandPushButton.sizePolicy().hasHeightForWidth())
        self.uiSPICECommandPushButton.setSizePolicy(sizePolicy)
        self.uiSPICECommandPushButton.setIcon(icon)
        self.uiSPICECommandPushButton.setObjectName("uiSPICECommandPushButton")
        self.horizontalLayout_10.addWidget(self.uiSPICECommandPushButton)
        self.gridLayout.addLayout(self.horizontalLayout_10, 5, 0, 1, 1)
        self.uiButtonBox = QtWidgets.QDialogButtonBox(self.uiCentralWidget)
        self.uiButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.uiButtonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Close|QtWidgets.QDialogButtonBox.Reset)
        self.uiButtonBox.setObjectName("uiButtonBox")
        self.gridLayout.addWidget(self.uiButtonBox, 6, 0, 1, 1)
        self.uiVNCCommandLabel.raise_()
        self.uiSPICECommandLabel.raise_()
        self.uiTelnetCommandLabel.raise_()
        self.uiButtonBox.raise_()
        MainWindow.setCentralWidget(self.uiCentralWidget)
        self.uiMenuBar = QtWidgets.QMenuBar(MainWindow)
        self.uiMenuBar.setGeometry(QtCore.QRect(0, 0, 913, 42))
        self.uiMenuBar.setObjectName("uiMenuBar")
        self.uiFileMenu = QtWidgets.QMenu(self.uiMenuBar)
        self.uiFileMenu.setObjectName("uiFileMenu")
        self.menu_Help = QtWidgets.QMenu(self.uiMenuBar)
        self.menu_Help.setObjectName("menu_Help")
        MainWindow.setMenuBar(self.uiMenuBar)
        self.uiAboutAction = QtWidgets.QAction(MainWindow)
        self.uiAboutAction.setMenuRole(QtWidgets.QAction.AboutRole)
        self.uiAboutAction.setObjectName("uiAboutAction")
        self.uiQuitAction = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/quit.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.uiQuitAction.setIcon(icon1)
        self.uiQuitAction.setObjectName("uiQuitAction")
        self.uiOnlineHelpAction = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/help.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.uiOnlineHelpAction.setIcon(icon2)
        self.uiOnlineHelpAction.setObjectName("uiOnlineHelpAction")
        self.uiAboutQtAction = QtWidgets.QAction(MainWindow)
        self.uiAboutQtAction.setMenuRole(QtWidgets.QAction.AboutQtRole)
        self.uiAboutQtAction.setObjectName("uiAboutQtAction")
        self.uiFileMenu.addAction(self.uiQuitAction)
        self.menu_Help.addAction(self.uiOnlineHelpAction)
        self.menu_Help.addAction(self.uiAboutAction)
        self.menu_Help.addAction(self.uiAboutQtAction)
        self.uiMenuBar.addAction(self.uiFileMenu.menuAction())
        self.uiMenuBar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(MainWindow)
        self.uiQuitAction.triggered.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GNS3 WebClient pack"))
        self.uiTelnetCommandPushButton.setText(_translate("MainWindow", "&Edit"))
        self.uiVNCCommandLabel.setText(_translate("MainWindow", "VNC command:"))
        self.uiVNCCommandPushButton.setText(_translate("MainWindow", "&Edit"))
        self.uiSPICECommandLabel.setText(_translate("MainWindow", "SPICE command:"))
        self.uiTelnetCommandLabel.setText(_translate("MainWindow", "Telnet command:"))
        self.uiSPICECommandPushButton.setText(_translate("MainWindow", "&Edit"))
        self.uiFileMenu.setTitle(_translate("MainWindow", "&File"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        self.uiAboutAction.setText(_translate("MainWindow", "&About"))
        self.uiAboutAction.setStatusTip(_translate("MainWindow", "About"))
        self.uiQuitAction.setText(_translate("MainWindow", "&Quit"))
        self.uiQuitAction.setStatusTip(_translate("MainWindow", "Quit"))
        self.uiQuitAction.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.uiOnlineHelpAction.setText(_translate("MainWindow", "&Online help"))
        self.uiOnlineHelpAction.setToolTip(_translate("MainWindow", "Online help"))
        self.uiOnlineHelpAction.setStatusTip(_translate("MainWindow", "Online Help"))
        self.uiAboutQtAction.setText(_translate("MainWindow", "About &Qt"))
        self.uiAboutQtAction.setStatusTip(_translate("MainWindow", "About Qt"))
from . import resources_rc
