#!./venv/bin/python3

import os
import sys
import requests
import time
import key

from retriever_photo_information import RetrieverPhotoInformation


class Sorter:
        def __init__(self):
            pass

        @staticmethod
        def get_location(lat, lon):
            if not lat and not lon:
                return None

            URL = 'https://api.opencagedata.com/geocode/v1/json'
            params = {
                "q": str(lat) + ' ' + str(lon),
                "key": key.key
            }
            request = requests.get(url=URL, params=params)

            # Condition of the free trial of the service: I can use API one time per second
            time.sleep(1.1)

            return {
                'country': request.json()['results'][0]['components']['country'],
                'city': request.json()['results'][0]['components']['city']
            }


if __name__ == '__main__':
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = '.'
    count = 10
    
    print(os.listdir(path))
