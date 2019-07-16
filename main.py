import sys
import os
from PySide2.QtWidgets import QApplication, QMainWindow, QPlainTextEdit
from PySide2.QtCore import QFile
from interface.main_window import Ui_MainWindow
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal

from sorter import Sorter
from sort_thread import SortThread


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.start = False
        self.sort_by_city = False
        self.sort_by_date = False
        self.sort_subdir = False

        self.ui.pushButton_Start.clicked.connect(self.startSort)
        self.ui.pushButton_Stop.clicked.connect(self.stopSort)
        self.ui.pushButton_dialog.clicked.connect(self.openDialog)
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.hide()
        self.sorter = SortThread()
        self.sorter.signal_log.connect(self.addLog)
        
    def checkOptions(self):
        self.sort_by_city = self.ui.checkBox_byCity.isChecked()
        self.sort_by_date = self.ui.checkBox_byDate.isChecked()
        self.sort_subdir = self.ui.checkBox_scanSubDir.isChecked()
        self.sorter.setOptions(self.sort_by_city, self.sort_by_date, self.sort_subdir)

    def openDialog(self):
        self.ui.openFileNameDialog()

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
        self.ui.checkBox_byCity.setDisabled(my_bool)
        self.ui.checkBox_byDate.setDisabled(my_bool)
        self.ui.checkBox_scanSubDir.setDisabled(my_bool)

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

    def getAmountElements(self, dir_name):
        try:
            amount = len(os.listdir(dir_name))
            return amount
        except FileNotFoundError as ef:
            self.log.addLog(ef)
            return None

    def addLog(self, text):
        current_value = self.ui.progressBar.value()
        self.ui.progressBar.setValue(current_value + 1)
        self.ui.plainTextEdit_logi.insertPlainText(text + '\n')

    def startSort(self):        
        api_key = self.ui.plainTextEdit.toPlainText()
        dir_name = self.ui.plainTextEdit_pathDir.toPlainText()
        self.sorter.setApiKey(api_key)
        test_request = Sorter.test_request(api_key)

        if test_request['code'] == 401:
            self.addLog(test_request['message'])
        elif self.isStarted():
            self.checkOptions()
            amount_elements = self.getAmountElements(dir_name)
            self.ui.progressBar.setMaximum(amount_elements)
            self.sorter.setPath(self.ui.plainTextEdit_pathDir.toPlainText())
            self.sorter.start()

    def stopSort(self):
        self.switchMode()
        self.sorter.stop()
        self.ui.progressBar.setValue(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
