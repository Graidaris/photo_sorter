# -*- coding: utf-8 -*-

import os
import json

class Session:
    def __init__(self):
        self.file = "session.json"
        self.file_js = {}
        
        if not os.path.exists(self.file):
            self.__createFile()
        else:
            self.__loadLastSession()
                
    def __loadLastSession(self):
        with open(self.file , 'r') as file:
            self.file_js = json.load(file)
            
    def __createFile(self):
        file = open(self.file, "w")
        file.close()
        
    def getData(self):
        return self.file_js
    
    def saveSession(self, data):
        with open(self.file, 'w') as target:
            json.dump(data, target)