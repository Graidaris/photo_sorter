# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal, QThread
from phsorter import PhSorter, RequestError

class Log:
    def __init__(self, signal):
        self.signal = signal

    def addLog(self, text):
        self.signal.emit(text)


class PathNotSetException(Exception):
    pass

class SortThread(QThread):
    signal_log = pyqtSignal(str)
    signal_endWork = pyqtSignal()
    signal_count_elements = pyqtSignal()

    def __init__(self):
        QThread.__init__(self)
        self.__sorter = PhSorter()
        self.loger = Log(self.signal_log)
        self.__sorter.setLog(self.loger)
        self.path = None

    def __del__(self):
        self.wait()

    def stop(self):
        self.__sorter.stop()
        self.wait()
        
    def setOptions(self, city = False, date = False, subdirectories = False, del_trash = False):
        """
        Set options, mean sort by ...
        """
        self.__sorter.setOptions(city, date, subdirectories, del_trash)

    def setApiKey(self, key: str):
        self.__sorter.setKeyAPI(key)

    def setPath(self, path: str):
        self.path = path

    def sendProgress(self):
        self.signal_count_elements.emit()

    def run(self):
        if self.path is None:
            raise PathNotSetException("You forgot to set a path.")
        
        self.__sorter.setProgressMon(self.sendProgress)
        self.__sorter.sort_files(self.path)        
        self.signal_endWork.emit()
