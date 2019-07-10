#!./venv/bin/python3

import PIL.Image
import PIL.ExifTags

class NotPhotoType(OSError):
    pass

class HasntGPSData(KeyError):
    pass


class RetrieverPhotoInformation:

    def __init__(self, name_file):
        if not self.is_photo(name_file):
            raise NotPhotoType
        
        self.photo_name = name_file
        img = PIL.Image.open(name_file)
        try:
            self.exif = {
                PIL.ExifTags.TAGS[k]: v
                for k, v in img._getexif().items()
                if k in PIL.ExifTags.TAGS
            }
        except AttributeError:
            self.exif = None
        

    @staticmethod
    def dms_to_dd(d, m, s, direction):
        dd = float(d) + (float(m) / 60.0) + (float(s) / 3600.0)
        if direction.upper() in "SW":
            dd *= -1
        return dd
    
    def is_photo(self, photo_name):
        return photo_name.split('.')[-1].lower() in ['jpg']
            

    def __transform_gps_data(self, source):
        return [val/div for val, div in source]

    def get_coordinates(self):
        if self.exif is None:
            return None
        
        latitude = 2
        longitude = 4
        pos_cord_dir_lat = 1
        pos_cord_dir_lon = 3

        try:
            gps_data = self.exif['GPSInfo']
        except KeyError:
            raise HasntGPSData

        cord = {
            'lat': {
                'val': self.__transform_gps_data(gps_data[latitude]),
                'dir': gps_data[pos_cord_dir_lat]
            },

            'lon': {
                'val': self.__transform_gps_data(gps_data[longitude]),
                'dir': gps_data[pos_cord_dir_lon]
            }
        }

        lat = self.dms_to_dd(
            cord['lat']['val'][0],  # degree
            cord['lat']['val'][1],  # minutes
            cord['lat']['val'][2],  # seconds
            cord['lat']['dir']  # direction
        )

        lon = self.dms_to_dd(
            cord['lon']['val'][0],  # degree
            cord['lon']['val'][1],  # minutes
            cord['lon']['val'][2],  # seconds
            cord['lon']['dir']  # direction
        )

        return {
            'lat': lat,
            'lon': lon
        }

    def get_date(self):
        date, time = self.exif['DateTimeOriginal'].split(' ')
        date, time = date.split(':'), time.split(':')
        return {
            'year': date[0],
            'month': date[1],
            'day': date[2],
            'hour': time[0],
            'minute': time[1],
            'second': time[2]
        }
