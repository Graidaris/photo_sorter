from os.path import isfile
from os.path import join as path_join
from os import listdir

from RetrieverGPS import RetrieverGPS

path = 'OneDrive-2019-05-15'

retriver_inform = RetrieverPhotoInformation()

count = 0
count_correct_processed = 0
count_error_processed = 0
count_not_correct_format = 0

with open('coordinats.txt', 'w') as file_to_write:

    for f in listdir(path):
        count += 1
        if f.split('.')[-1] == 'jpg':
            cord = retriver_inform.extract_coord(path_join(path, f))
            if cord is not None:
                count_correct_processed += 1
                file_to_write.write(str(cord) + '\n')
            else:
                count_error_processed += 1
        else:
            count_not_correct_format += 1


print('Complite!\n'
      f'All file is processed: {count}\n'
      f"Files has benn processed correct: {count_correct_processed}\n"
      f"Files has been processed with error: {count_error_processed}\n"
      f"Files has been not correct format: {count_not_correct_format}\n"
      )
