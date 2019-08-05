from PyQt5.QtCore import pyqtSignal, QThread
from sorter import Sorter, RequestError

class Log:
    def __init__(self, signal):
        self.signal = signal

    def addLog(self, text):
        self.signal.emit(text)
        
class PathNotSetException(Exception):
    pass

class SortThread(QThread):
    signal_log = pyqtSignal(str)

    def __init__(self):
        QThread.__init__(self)
        self.__sorter = Sorter()        
        loger = Log(self.signal_log)
        self.__sorter.setLog(loger)
        self.path = None

    def __del__(self):
        self.wait()

    def stop(self):
        self.__sorter.stop()
        self.wait()
        
    def setOptions(self, city = False, date = False, subdirectories = False):
        """
        Set options, mean sort by ...
        """
        self.__sorter.setOptions(city, date, subdirectories)

    def setApiKey(self, key: str):
        self.__sorter.setKeyAPI(key)

    def setPath(self, path: str):
        self.path = path

    def run(self):
        if self.path is None:
            raise PathNotSetException("You forgot to set a path.")
        
        try:
            self.__sorter.sort_files(self.path)
        except RequestError:
            raise RequestError
