#!./venv/bin/python3

import os
import sys
import requests
import time


'''
I use opencagedata service
My accesses key for API of the service
'''
import key
from retriever_photo_information import RetrieverPhotoInformation

try:
    path = sys.argv[1]
except IndexError as e:
    path = '.'

URL = 'https://api.opencagedata.com/geocode/v1/json'
count = 0
count_correct_processed = 0
count_error_processed = 0
count_not_correct_format = 0

with open('coordinats.txt', 'w') as file_to_write:
    for f in os.listdir(path):
        if count > 100:
            #test limit
            print("Limit crossed of 100 photos!")
            break
        count += 1
        if f.split('.')[-1] == 'jpg':
            photo = RetrieverPhotoInformation(os.path.join(path, f))
            cord = photo.get_coordinates()
            if cord is not None:
                count_correct_processed += 1
                params = {"q": str(cord['lat']) + ' ' + str(cord['lon']),
                          "key": key.key}

                r = requests.get(url=URL, params=params)
                text_to_write = f + ' ' + r.json()['results'][0]['components']['country'] + ' ' + \
                                r.json()['results'][0]['components']['city'] + '\n'

                print(text_to_write, end='')

                file_to_write.write(text_to_write)
            else:
                count_error_processed += 1
        else:
            count_not_correct_format += 1

        """Condition of the free trial of the service: I can use API one time per second"""
        time.sleep(1.1)

print('Complete!\n'
      f'All file is processed: {count}\n'
      f"Files has benn processed correct: {count_correct_processed}\n"
      f"Files has been processed with error: {count_error_processed}\n"
      f"Files has been not correct format: {count_not_correct_format}\n"
      )
