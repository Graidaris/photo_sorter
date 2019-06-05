#!/usr/bin/python3

import os
import sys

from retriever_photo_information import RetrieverPhotoInformation

try:
    path = sys.argv[1]
except IndexError as e:
    path = '.'

count = 0
count_correct_processed = 0
count_error_processed = 0
count_not_correct_format = 0

with open('coordinats.txt', 'w') as file_to_write:
    for f in os.listdir(path):
        count += 1
        if f.split('.')[-1] == 'jpg':
            photo = RetrieverPhotoInformation(os.path.join(path, f))
            cord = photo.get_coordinates()
            if cord is not None:
                count_correct_processed += 1
                file_to_write.write(str(cord) + '\n')
            else:
                count_error_processed += 1
        else:
            count_not_correct_format += 1

print('Complete!\n'
      f'All file is processed: {count}\n'
      f"Files has benn processed correct: {count_correct_processed}\n"
      f"Files has been processed with error: {count_error_processed}\n"
      f"Files has been not correct format: {count_not_correct_format}\n"
      )
