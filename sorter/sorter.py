# -*- coding: utf-8 -*-

import os
from os.path import join
import requests
import time

from sorter.sort_exeption import SortError
from sorter.extractor import ExtractorExif, NotPhotoType, HasntGPSData
from sorter.log import Log
from sorter.service import ServiceAPI, RequestError

def getAmountElements(path: str) -> int:
        count_file = 0
        for file in os.listdir(path):
            full_name = os.path.join(path, file)
            if os.path.isfile(full_name):
                count_file += 1
            elif os.path.isdir(full_name):
                count_file += getAmountElements(full_name)
                
        return count_file

class Sorter:
    def __init__(self):
        self.__log = Log()
        self.stoped = False
        self.sort_by_city = False
        self.sort_by_date = False
        self.sort_subdir = False  #subd is subdirection
        self.del_trash_opt = False
        self.service_API = ServiceAPI()
        self.root_dir = None
        self.progressMon = None

    def setKeyAPI(self, key):
        self.service_API.set_api_key(key)
        
    def setProgressMon(self, func):
        """
        Set a function for monitoring the progress
        """
        self.progressMon = func

    def setLog(self, log):
        self.__log = log

    def stop(self):
        self.stoped = True

    def setOptions(self,
                   sort_by_city=False,
                   sort_by_date=False,
                   sort_by_subd=False,
                   delete_trash=False):

        self.sort_by_city = sort_by_city
        self.sort_by_date = sort_by_date
        self.sort_subdir = sort_by_subd
        self.del_trash_opt = delete_trash

    def delete_folder(self, path):
        try:
            os.rmdir(path)
        except OSError:
            pass

    def delete_trash(self, path):
        """
        Deletes empty folders
        """
        for element in os.listdir(path):
            full_name = os.path.join(path, element)
            if os.path.isdir(full_name):
                self.delete_trash(full_name)
        self.delete_folder(path) 

    def createDir(self, target_dir, name):
        if name is not None:
            target_dir = join(target_dir, name)
            if not os.path.exists(target_dir):
                os.mkdir(target_dir)
        return target_dir

    def _update_photo_info(self, full_name):
        try:
            photo_exif_info = ExtractorExif(full_name)
            coord = photo_exif_info.get_coordinates()
            self.service_API.update_data(coord['lat'], coord['lon'])

        except HasntGPSData:
            self.__log.addLog(f"{full_name} hasnt GPS data")
            raise SortError
        except NotPhotoType:
            self.__log.addLog(f"File {full_name} is not a photo")
            raise SortError
        except TypeError:
            raise SortError
            self.__log.addLog(f"Type error {full_name}")

    def _moveFileToDir(self, path, file_name):
        full_name = join(path, file_name)        
        try:
            self._update_photo_info(full_name)
        except SortError:
            return

        target_dir = self.root_dir
        target_dir = self.createDir(target_dir, self.service_API.get_country())

        if self.sort_by_city:
            target_dir = self.createDir(target_dir, self.service_API.get_city())

        target_dir = join(target_dir, file_name)
        os.rename(full_name, target_dir)
        self.__log.addLog(full_name + " has changed the name to " + target_dir)
        

    def progressUpdate(self):
        if self.progressMon is not None:
            self.progressMon()
    
    def _sort(self, path):
        for file_name in os.listdir(path):
            if self.stoped:
                self.__log.addLog("Sorter has been stoped...")
                return

            full_file_name = os.path.join(path, file_name)
            object_is_dir = os.path.isdir(full_file_name)

            if object_is_dir and self.sort_subdir:
                new_path = os.path.join(path, file_name)
                self._sort(new_path)
            else:                
                self._moveFileToDir(path, file_name)
                self.progressUpdate()
    
    def check_api_key(self):
        try:
            self.service_API.check_api_key()
        except RequestError as error:
            self.__log.addLog(error.__str__())
            raise error

    def valid_path(self, path):
        if path == "" or path == None:
            self.__log.addLog("You forgot to set a path")
            raise OSError

    def sort_files(self, path: str):
        self.check_api_key()
        self.valid_path(path)
        
        path = path.replace("/", "\\")
        self.root_dir = path
        self.stoped = False
        self._sort(path)
        if self.del_trash_opt:
            self.delete_trash(self.root_dir)
        self.__log.addLog("Done...\n\n\n")
