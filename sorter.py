#!./venv/bin/python3

import os
from os.path import join
import requests
import time

from retriever_photo_info import RetrieverPhotoInformation, NotPhotoType, HasntGPSData

'''
I use 'opencagedata' service
'''

class NotApiException(Exception):
    pass

class Log:
    def __init__(self):
        pass

    def addLog(self, text):
        print(text)


class Sorter:
    def __init__(self):
        self.__log = Log()
        self.__api_key = None
        self.stoped = False
        self.sort_by_city = False
        self.sort_by_date = False
        self.sort_subd = False #subd is subdirection

    def setLog(self, log):
        self.__log = log
        
    def stop(self):
        self.stoped = True

    def setKeyAPI(self, api_key):
        self.__api_key = api_key
        
    def setOptions(self, sort_by_city = False, sort_by_date = False, sort_by_subd = False):
        self.sort_by_city = sort_by_city
        self.sort_by_date = sort_by_date
        self.sort_subd = sort_by_subd

    def get_location(self, lat, lon):
        if not lat or not lon:
            return None

        URL = 'https://api.opencagedata.com/geocode/v1/json'
        params = {
            "q": str(lat) + ' ' + str(lon),
            "key": self.__api_key
        }
        request = requests.get(url=URL, params=params)

        # Condition of the free trial of the service: I can use API one time per second
        time.sleep(1.1)
        location = {}
        try:
            location['country'] = request.json()['results'][0]['components']['country']
        except KeyError:
            location['country'] = None

        try:
            location['city'] = request.json()['results'][0]['components']['city']
        except KeyError:
            location['city'] = None

        return location

    @staticmethod
    def test_request(api):
        URL = 'https://api.opencagedata.com/geocode/v1/json'
        #test request, London latlon
        params = {
            "q": str(51.528583) + ' ' + str(-0.192254),
            "key": api
        }
        request = requests.get(url=URL, params=params)
        return request.json()["status"]
    
    def createDir(self, location, key, target_dir):
        if location[key] is not None:
            target_dir = join(target_dir, location[key])
            if not os.path.exists(target_dir):
                os.mkdir(target_dir)
        return target_dir
                
    def sortDir(self, path, file = ''):
        path = os.path.join(path, file)
        if path is not None:
            for file_name in os.listdir(os.path.join(path, file)):
                if self.stoped:
                    self.__log.addLog("Sorter has been stoped...")
                    return
                if os.path.isdir(path) and self.sort_subd:
                    self.sortDir(path, file_name)
                else:
                    self.moveFileToDir(path, file_name)
                    
    def moveFileToDir(self, path, file_name):
        if path is not None:
            try:
                photo_exif_info = RetrieverPhotoInformation(join(path, file_name))
                coord = photo_exif_info.get_coordinates()
                location = self.get_location(coord['lat'], coord['lon'])
                
                target_dir = path                
                target_dir = self.createDir(location, 'country', target_dir)
                target_dir = self.createDir(location, 'city', target_dir)

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
        if self.__api_key is None:
            self.__log.addLog("You forgot put api key.")
            raise NotApiException("You forgot to set the API key")
        
        self.stoped = False
        self.sortDir(path)
        self.__log.addLog("Done...\n\n\n")
