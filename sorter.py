#!./venv/bin/python3

import os
from os.path import join
import sys
import requests
import time
import privat

from retriever_photo_information import RetrieverPhotoInformation


class Sorter:
    def __init__(self, path):
        self.PATH=path
    
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
        
    def sort_files(self):
        if not os.path.isdir(self.PATH):
            return None
        
        for photo in os.listdir(self.PATH):
            
            if not RetrieverPhotoInformation.is_photo(photo):
                continue
            
            photo_exif_info = RetrieverPhotoInformation(join(self.PATH, photo))
            coord = photo_exif_info.get_coordinates()
            if coord is None:
                continue
            
            location = self.get_location(coord['lat'], coord['lon'])                
            if location is None:
                continue
            
            target_dir = ""
            if location['country'] is None:
                continue
            
            target_dir = join(self.PATH, location['country'])
            if not os.path.exists(target_dir):
                os.mkdir(target_dir)
            
            if location['city'] is not None:
                target_dir = join(target_dir, location['city'])
                if not os.path.exists(target_dir):
                    os.mkdir(target_dir)
                    
            os.rename(join(self.PATH, photo), join(target_dir, photo))
            print(join(self.PATH, photo), "has change name to", join(target_dir, photo))
                
                


if __name__ == '__main__':
    path = privat.path
    sorter = Sorter(path)
    sorter.sort_files()
    
