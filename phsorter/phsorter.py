# -*- coding: utf-8 -*-

import os
import requests
import time

from phsorter.sort_exeption import SortError
from phsorter.extractor import ExtractorExif, NotPhotoType, HasntGPSData
from phsorter.log import Log
from phsorter.service import ServiceAPI, RequestError


class PhSorter:
    def __init__(self):
        self.__log = Log()
        self.current_photo_info = None
        self.stoped = False
        self.sort_by_country = False
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
                   sort_by_country=False,
                   sort_by_city=False,
                   sort_by_date=False,
                   sort_by_subd=False,
                   delete_trash=False):

        self.sort_by_country = sort_by_country
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

    def progressUpdate(self):
        if self.progressMon is not None:
            self.progressMon()

    def createDir(self, target_dir, name) -> str:
        """
        Creates a new directory and return new full path of the directory 
        """
        if name is not None:
            target_dir = os.path.join(target_dir, name)
            if not os.path.exists(target_dir):
                os.mkdir(target_dir)
        return target_dir
    
    

    def _update_photo_info(self, full_name):
        try:
            photo_exif_info = ExtractorExif(full_name)
            self.current_photo_info = {}
            
            if self.sort_by_city or self.sort_by_country:
                coord = photo_exif_info.get_coordinates()
                self.service_API.update_data(coord['lat'], coord['lon'])
            
                if self.sort_by_country:
                    self.current_photo_info['country'] = self.service_API.get_country()
                if self.sort_by_city:
                    self.current_photo_info['city'] = self.service_API.get_city()
            if self.sort_by_date:
                self.current_photo_info['date'] = photo_exif_info.get_date()            
            
        except HasntGPSData:
            self.__log.addLog(f"{full_name} hasnt GPS data")
            raise SortError
        except NotPhotoType:
            self.__log.addLog(f"File {full_name} has an unsupported format")
            raise SortError
        except TypeError:
            self.__log.addLog(f"Type error {full_name}")
            raise SortError
        except KeyError as error:
            self.__log.addLog(str(error))
            raise SortError

    def _moveFileToDir(self, path, file_name):
        full_name = os.path.join(path, file_name)
        try:
            self._update_photo_info(full_name)
        except SortError:
            return

        target_dir = self.root_dir
        
        if self.current_photo_info.get('country'):
            target_dir = self.createDir(target_dir, self.current_photo_info.get('country'))

        if self.current_photo_info.get('city'):
            target_dir = self.createDir(target_dir, self.current_photo_info.get('city'))

        if self.current_photo_info.get('date'):
            date_photo = self.current_photo_info.get('date')
            new_dir_name = (str(date_photo['year']) + '-' +
                            str(date_photo['month']) + '-' +
                            str(date_photo['day']))
            target_dir = self.createDir(target_dir, new_dir_name)

        target_dir = os.path.join(target_dir, file_name)
        os.rename(full_name, target_dir)
        self.__log.addLog(full_name + " has changed the name to " + target_dir)

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

    def valid_path(self, path):
        if path == "" or path == None:
            self.__log.addLog("You forgot to set a path")
            raise OSError("Error: The path is invalid")

    def check_api_key(self):
        try:
            self.service_API.check_api_key()
        except RequestError as error:
            self.__log.addLog(error.__str__())
            raise error

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
