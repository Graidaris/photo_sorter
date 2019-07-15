#!./venv/bin/python3

import os
from os.path import join
import sys
import requests
import time

from retriever_photo_information import RetrieverPhotoInformation, NotPhotoType, HasntGPSData

'''
I use 'opencagedata' service
My accesses key for API of the service
'''


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

    def setLog(self, log):
        self.__log = log
        
    def stop(self):
        self.stoped = True

    def setKeyAPI(self, api_key):
        self.__api_key = api_key

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

    def sort_files(self, path):
        if not os.path.isdir(path):
            return None

        if self.__api_key is None:
            self.__log.addLog("You forgot put api key.")
            return None
        
        self.stoped = False

        for photo in os.listdir(path):
            if self.stoped:
                self.__log.addLog("Sorter has been stoped...")
                return
            
            if not os.path.isfile(join(path, photo)):
                continue

            try:
                photo_exif_info = RetrieverPhotoInformation(join(path, photo))
                coord = photo_exif_info.get_coordinates()
                location = self.get_location(coord['lat'], coord['lon'])
                target_dir = ""
                target_dir = join(path, location['country'])

                if not os.path.exists(target_dir):
                    os.mkdir(target_dir)

                if location['city'] is not None:
                    target_dir = join(target_dir, location['city'])
                    if not os.path.exists(target_dir):
                        os.mkdir(target_dir)

                os.rename(join(path, photo), join(target_dir, photo))
                self.__log.addLog(
                    join(path, photo) + " has change name to " + join(target_dir, photo)
                )

            except HasntGPSData:
                self.__log.addLog(f"{photo} hasnt GPS data")
            except NotPhotoType:
                self.__log.addLog(f"File {photo} is not a photo")
            except TypeError:
                self.__log.addLog(f"Type error {photo}")

        self.__log.addLog("Done...\n\n\n")
