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
            if not lat and not lon:
                return None

            URL = 'https://api.opencagedata.com/geocode/v1/json'
            params = {
                "q": str(lat) + ' ' + str(lon),
                "key": privat.key
            }
            request = requests.get(url=URL, params=params)

            # Condition of the free trial of the service: I can use API one time per second
            time.sleep(1.1)

            return {
                'country': request.json()['results'][0]['components']['country'],
                'city': request.json()['results'][0]['components']['city']
            }
            
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
                
                dir_country = join(self.PATH, location['country'])
                dir_city = join(dir_country, location['city'])
                
                if not os.path.exists(dir_country):
                    os.mkdir(dir_country)
                    os.mkdir(dir_city)
                else:
                    if not os.path.exists(dir_city):
                        os.mkdir(dir_city)
                
                os.rename(join(self.PATH, photo), join(dir_city, photo))
                print(join(self.PATH, photo), "has change name to", join(dir_city, photo))


if __name__ == '__main__':
    path = privat.path
    sorter = Sorter(path)
    sorter.sort_files()
    
