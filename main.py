import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QPlainTextEdit
from PySide2.QtCore import QFile
from interface.main_window import Ui_MainWindow

from sorter import Sorter
from log_sorter import LogSorter


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.log = LogSorter()
        self.log.setWidgetLog(self.ui.plainTextEdit_logi)
        
        self.sorter = Sorter()
        self.sorter.setLog(self.log)
        
        self.ui.pushButton_Start.clicked.connect(self.startSort)
        
    def startSort(self):
        api_key = self.ui.plainTextEdit.toPlainText()
        dir_name = self.ui.plainTextEdit_pathDir.toPlainText()
        
        self.sorter.setKeyAPI(api_key)
        test_request = self.sorter.test_request()
        if test_request['code'] == 401:
            self.log.addLog(test_request['message'])
        else:
            self.sorter.sort_files(dir_name)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
