# -*- coding: utf-8 -*-

import os
import json


class Session:
    def __init__(self):
        self.__FILE_NAME = "session.json"
        self.__PATH_CASH = "cash"
        self.__FILE_PATH = os.path.join(self.__PATH_CASH, self.__FILE_NAME)
        
        self.file_js = {}
        self.create_cash_dir()
        self.__loadLastSession()

    def __loadLastSession(self):
        if not os.path.exists(self.__FILE_PATH):
            self.__createFile()
        else:
            with open(self.__FILE_PATH, 'r') as file:
                self.file_js = json.load(file)

    def __createFile(self):
        file = open(self.__FILE_PATH, "w")
        file.close()

    def getData(self, key):        
        return self.file_js.get(key)

    def saveSession(self, data):
        if not os.path.exists(self.__FILE_PATH):
            raise FileNotFoundError

        with open(self.__FILE_PATH, 'w') as target:
            json.dump(data, target)

    def write_date(self, key, data, hash=False):
        self.file_js[key] = data

    def create_cash_dir(self):
        if os.path.exists(self.__PATH_CASH):
            pass
        else:
            os.makedirs(self.__PATH_CASH)
            
    def delete_session(self):
        if os.path.exists(self.__FILE_PATH):
            os.remove(self.__FILE_PATH)