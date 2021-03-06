# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui\main_window.ui',
# licensing of '.\ui\main_window.ui' applies.
#
# Created: Sat Jul 13 13:16:27 2019
#      by: pyside2-uic  running on PySide2 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
import PySide2

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(547, 370)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(547, 370))
        MainWindow.setMaximumSize(QtCore.QSize(547, 370))
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.plainTextEdit_logi = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_logi.setGeometry(QtCore.QRect(10, 160, 521, 171))
        self.plainTextEdit_logi.setReadOnly(True)
        self.plainTextEdit_logi.setObjectName("plainTextEdit_logi")
        self.pushButton_Start = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Start.setEnabled(True)
        self.pushButton_Start.setGeometry(QtCore.QRect(180, 100, 191, 61))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(20)
        font.setWeight(75)
        font.setBold(True)
        self.pushButton_Start.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/power-button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Start.setIcon(icon)
        self.pushButton_Start.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_Start.setFlat(True)
        self.pushButton_Start.setObjectName("pushButton_Start")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 60, 117, 68))
        self.layoutWidget.setObjectName("layoutWidget")
        self.options_layout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.options_layout.setContentsMargins(0, 0, 0, 0)
        self.options_layout.setObjectName("options_layout")
        self.checkBox_byCity = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox_byCity.setObjectName("checkBox_byCity")
        self.options_layout.addWidget(self.checkBox_byCity)
        self.checkBox_byDate = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox_byDate.setObjectName("checkBox_byDate")
        self.options_layout.addWidget(self.checkBox_byDate)
        self.checkBox_scanSubDir = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox_scanSubDir.setObjectName("checkBox_scanSubDir")
        self.options_layout.addWidget(self.checkBox_scanSubDir)
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 20, 521, 31))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.path_to_dir = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.path_to_dir.setContentsMargins(0, 0, 0, 0)
        self.path_to_dir.setObjectName("path_to_dir")
        self.plainTextEdit_pathDir = QtWidgets.QPlainTextEdit(self.layoutWidget1)
        self.plainTextEdit_pathDir.setUndoRedoEnabled(True)
        self.plainTextEdit_pathDir.setOverwriteMode(False)
        self.plainTextEdit_pathDir.setObjectName("plainTextEdit_pathDir")
        self.path_to_dir.addWidget(self.plainTextEdit_pathDir)
        self.pushButton_dialog = QtWidgets.QPushButton(self.layoutWidget1)
        self.pushButton_dialog.setObjectName("pushButton_dialog")
        self.path_to_dir.addWidget(self.pushButton_dialog)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(10, 340, 521, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.pushButton_Stop = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Stop.setEnabled(False)
        self.pushButton_Stop.setGeometry(QtCore.QRect(180, 100, 191, 61))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(20)
        font.setWeight(75)
        font.setBold(True)
        self.pushButton_Stop.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Stop.setIcon(icon1)
        self.pushButton_Stop.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_Stop.setFlat(True)
        self.pushButton_Stop.setObjectName("pushButton_Stop")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(140, 60, 341, 31))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.widget)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.horizontalLayout.addWidget(self.plainTextEdit)
        self.pushButton_Help = QtWidgets.QPushButton(self.widget)
        self.pushButton_Help.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/info.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Help.setIcon(icon2)
        self.pushButton_Help.setFlat(True)
        self.pushButton_Help.setObjectName("pushButton_Help")
        self.horizontalLayout.addWidget(self.pushButton_Help)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "Photo sorter", None, -1))
        self.pushButton_Start.setText(QtWidgets.QApplication.translate("MainWindow", "START", None, -1))
        self.checkBox_byCity.setText(QtWidgets.QApplication.translate("MainWindow", "sort by city", None, -1))
        self.checkBox_byDate.setText(QtWidgets.QApplication.translate("MainWindow", "sort by date", None, -1))
        self.checkBox_scanSubDir.setText(QtWidgets.QApplication.translate("MainWindow", "scan subdirectories", None, -1))
        self.pushButton_dialog.setText(QtWidgets.QApplication.translate("MainWindow", "Browser", None, -1))
        self.pushButton_Stop.setText(QtWidgets.QApplication.translate("MainWindow", "STOP", None, -1))
        self.plainTextEdit.setPlainText(QtWidgets.QApplication.translate("MainWindow", "Put here your API key", None, -1))
        self.pushButton_Stop.hide()

    def openFileNameDialog(self):
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            dirName = QFileDialog.getExistingDirectory( options=options)
            if dirName:
                self.plainTextEdit_pathDir.setPlainText(dirName)
                
    def getDirName(self):
        return self.plainTextEdit_pathDir.toPlainText()
    
    def writeToLog(self, text):    
        self.plainTextEdit_logi.insertPlainText(text)
        