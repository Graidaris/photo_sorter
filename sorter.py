#!./venv/bin/python3

import os
from os.path import join
import sys
import requests
import time
import privat

from retriever_photo_information import RetrieverPhotoInformation, NotPhotoType, HasntGPSData

'''
I use 'opencagedata' service
My accesses key for API of the service
'''

class LogSorter:
    def __init__(self):
        pass
    
    def addLog(self, text):
        print(text)

class Sorter:
    def __init__(self):
        self.log = LogSorter()
    
    def setLog(self, log):
        self.log = log    
    
    def get_location(self, lat, lon):
        if not lat or not lon:
            return None

        URL = 'https://api.opencagedata.com/geocode/v1/json'
        params = {
            "q": str(lat) + ' ' + str(lon),
            "key": privat.key
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
        
    def sort_files(self, path):
        if not os.path.isdir(path):
            return None
        
        for photo in os.listdir(path):
            if not os.path.isfile(join(path,photo)):
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
                self.log.addLog(join(path, photo) + " has change name to " + join(target_dir, photo))
                    
            except HasntGPSData:
                self.log.addLog(f"{photo} hasnt GPS data")
            except NotPhotoType:
                self.log.addLog(f"File {photo} is not a photo")
            except TypeError:
                self.log.addLog(f"Type error {photo}")
                
        self.log.addLog("Done...\n\n\n")


if __name__ == '__main__':
    path = privat.path
    sorter = Sorter()
    sorter.sort_files(path)
    
