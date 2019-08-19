# -*- coding: utf-8 -*-

import os
from os.path import join
import requests
import time

from sorter.extractor import ExtractorExif, NotPhotoType, HasntGPSData
from sorter.log import Log
from sorter.service import ServiceAPI, RequestError

class Sorter:
    def __init__(self):
        self.__log = Log()
        self.stoped = False
        self.sort_by_city = False
        self.sort_by_date = False
        self.sort_subd = False #subd is subdirection
        self.service_API = ServiceAPI()        

    def setLog(self, log):
        self.__log = log
        
    def stop(self):
        self.stoped = True

    def setKeyAPI(self, api_key):
        self.service_API.set_api_key(api_key)
        
    def setOptions(self, sort_by_city = False, sort_by_date = False, sort_by_subd = False):
        self.sort_by_city = sort_by_city
        self.sort_by_date = sort_by_date
        self.sort_subd = sort_by_subd
        
    def check_api_key(self, api_key: str):
        self.service_API.check_api_key(api_key)
    
    def createDir(self, name, target_dir):
        if name is not None:
            target_dir = join(target_dir, name)
            if not os.path.exists(target_dir):
                os.mkdir(target_dir)
        return target_dir
                
    def sort(self, path, file = ''):
        path = os.path.join(path, file)
        if path is not None:
            for file_name in os.listdir(os.path.join(path, file)):
                if self.stoped:
                    self.__log.addLog("Sorter has been stoped...")
                    return
                if os.path.isdir(path) and self.sort_subd:
                    self.sort(path, file_name)
                else:
                    self.moveFileToDir(path, file_name)
                    
    def moveFileToDir(self, path, file_name):
        if path is not None:
            try:
                photo_exif_info = ExtractorExif(join(path, file_name))
                coord = photo_exif_info.get_coordinates()
                
                self.service_API.update_data(coord['lat'], coord['lon'])
                
                target_dir = path
                target_dir = self.createDir(self.service_API.get_country(), target_dir)
                target_dir = self.createDir(self.service_API.get_city(), target_dir)

                os.rename(join(path, file_name), join(target_dir, file_name))
                self.__log.addLog(
                    join(path, file_name) + " has changed the name to " + join(target_dir, file_name)
                )

            except HasntGPSData:
                self.__log.addLog(f"{file_name} hasnt GPS data")
            except NotPhotoType:
                self.__log.addLog(f"File {file_name} is not a photo")
            except TypeError:
                self.__log.addLog(f"Type error {file_name}")
        
    
    def sort_files(self, path):
        try:
            self.service_API.check_api_key()            
        except RequestError as error:
            self.__log.addLog(error.__str__())
            return
        
        if path == "" or path == None:
            self.__log.addLog("You forgot to set a path")
            return
        
        self.stoped = False
        self.sort(path)
        self.__log.addLog("Done...\n\n\n")

