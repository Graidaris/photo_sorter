# -*- coding: utf-8 -*-

import sys
import os
from PySide2.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QMessageBox, QAction
from PySide2.QtCore import QFile
from interface.main_window import Ui_MainWindow
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal

from phsorter import getAmountElements
from sort_thread import SortThread, RequestError, PathNotSetException
from session import Session


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.start = False

        self.ui.pushButton_Start.clicked.connect(self.startSort)
        self.ui.pushButton_Stop.clicked.connect(self.stopSort)
        self.ui.pushButton_dialog.clicked.connect(self.openDialog)
        self.ui.pushButton_Help.clicked.connect(self.openHelpBox)

        self.ui.progressBar.setValue(0)
        self.ui.progressBar.hide()
        self.sorter = SortThread()
        self.sorter.signal_log.connect(self.addLog)
        self.sorter.signal_endWork.connect(self.stopSort)
        self.sorter.signal_count_elements.connect(self.updateProgressBar)

        self.session = Session()
        self.loadSession()

    def loadSession(self):
        cash_exists = False
        session_API = self.session.getData('API_key')
        session_dir = self.session.getData('path')

        if session_API is not None:
            self.ui.plainTextEdit.setPlainText(session_API)
            cash_exists = True

        if session_dir is not None:
            self.ui.plainTextEdit_pathDir.setPlainText(session_dir)
            cash_exists = True

        if cash_exists:
            self.ui.checkBox_saveSession.setChecked(True)

    def exit(self):
        if self.ui.checkBox_saveSession.isChecked():
            self.saveSession({
                'API_key':
                self.ui.plainTextEdit.toPlainText(),
                'path':
                self.ui.plainTextEdit_pathDir.toPlainText()
            })
        else:
            self.session.delete_session()

    def saveSession(self, data: dict):
        try:
            self.session.saveSession(data)
        except OSError as ex:
            self.addLog(ex)

    def checkOptions(self):
        sort_by_city = self.ui.checkBox_byCity.isChecked()
        sort_by_date = self.ui.checkBox_byDate.isChecked()
        sort_subdir = self.ui.checkBox_scanSubDir.isChecked()
        del_trash = False

        self.sorter.setOptions(sort_by_city, sort_by_date, sort_subdir,
                               del_trash)

    def openDialog(self):
        self.ui.openFileNameDialog()

    def openHelpBox(self):
        header = "Help window"
        text = "To get the api key you need visit https://opencagedata.com/"
        QMessageBox.question(self, header, text, QMessageBox.Close)

    def isStarted(self):
        self.switchMode()
        return self.start

    def disableUI(self, my_bool):
        self.ui.plainTextEdit_pathDir.setDisabled(my_bool)
        self.ui.plainTextEdit.setDisabled(my_bool)
        self.ui.progressBar.setDisabled(not my_bool)
        self.ui.pushButton_Start.setDisabled(my_bool)
        self.ui.pushButton_Stop.setDisabled(not my_bool)
        self.ui.pushButton_dialog.setDisabled(my_bool)
        self.ui.pushButton_Help.setDisabled(my_bool)
        self.ui.checkBox_byCity.setDisabled(my_bool)
        self.ui.checkBox_byDate.setDisabled(my_bool)
        self.ui.checkBox_scanSubDir.setDisabled(my_bool)
        self.ui.checkBox_saveSession.setDisabled(my_bool)

    def switchMode(self):
        if self.start:
            self.start = False
        else:
            self.start = True

        self.disableUI(self.start)

        if self.start:
            self.ui.pushButton_Start.hide()
            self.ui.pushButton_Stop.show()
            self.ui.progressBar.show()
        else:
            self.ui.pushButton_Start.show()
            self.ui.pushButton_Stop.hide()
            self.ui.progressBar.hide()

    def updateProgressBar(self):
        current_value = self.ui.progressBar.value()
        self.ui.progressBar.setValue(current_value + 1)

    def addLog(self, text):
        self.ui.plainTextEdit_logi.insertPlainText(text + '\n')

    def startSort(self):
        api_key = self.ui.plainTextEdit.toPlainText()
        dir_name = self.ui.plainTextEdit_pathDir.toPlainText()
        self.sorter.setApiKey(api_key)

        if self.isStarted():
            self.checkOptions()
            amount_elements = getAmountElements(dir_name)
            self.ui.progressBar.setMaximum(amount_elements)
            self.sorter.setPath(dir_name)

            try:
                self.sorter.start()
            except PathNotSetException as error:
                self.addLog(error)
            except RequestError as error:
                self.addLog(error)

    def stopSort(self):
        self.switchMode()
        self.sorter.stop()
        self.ui.progressBar.setValue(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    if app.exec_() == 0:
        window.exit()
        sys.exit(0)
