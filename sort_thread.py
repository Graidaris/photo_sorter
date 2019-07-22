from PyQt5.QtCore import pyqtSignal, QThread
from sorter import Sorter, NotApiException

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
        
    def setOptions(self, city = False, date = False, subd = False):
        self.sorter.setOptions(city, date, subd)

    def setApiKey(self, key):
        self.sorter.setKeyAPI(key)

    def setPath(self, path):
        self.path = path

    def run(self):
        try:
            self.sorter.sort_files(self.path)
        except NotApiException:
            print("Api not found")
        