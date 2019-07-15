import sys
import os
from PySide2.QtWidgets import QApplication, QMainWindow, QPlainTextEdit
from PySide2.QtCore import QFile
from interface.main_window import Ui_MainWindow
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal

from sorter import Sorter

class Log:
        def __init__(self, signal):
            self.signal = signal

        def addLog(self, text):
            self.signal.emit(text)

class SortThread(QThread):
    signal_log = pyqtSignal(str)
    
    def __init__(self):
        QThread.__init__(self)
        self.sorter = Sorter()
        loger = Log(self.signal_log)
        self.sorter.setLog(loger)
        self.api_key = None
        self.path = None

    def __del__(self):
        self.wait()
        
    def stop(self):
        self.sorter.stop()
        self.wait()
        
    def setApiKey(self, key):
        self.sorter.setKeyAPI(key)
        
    def setPath(self, path):
        self.path = path

    def run(self):
        self.sorter.sort_files(self.path)        
    


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.start = False

        self.ui.pushButton_Start.clicked.connect(self.startSort)
        self.ui.pushButton_Stop.clicked.connect(self.stopSort)
        self.ui.pushButton_dialog.clicked.connect(self.openDialog)
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.hide()
        self.sorter = SortThread()
        self.sorter.signal_log.connect(self.addLog)
        
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
        
        if my_bool:
            self.ui.pushButton_Start.hide()        
            self.ui.pushButton_Stop.show()
            self.ui.progressBar.show()
        else:
            self.ui.pushButton_Start.show()        
            self.ui.pushButton_Stop.hide()
            self.ui.progressBar.hide()

    def switchMode(self):
        if self.start:
            self.start = False
        else:
            self.start = True
            
        self.disableUI(self.start)

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
