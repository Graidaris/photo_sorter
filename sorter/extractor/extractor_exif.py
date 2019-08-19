# -*- coding: utf-8 -*-

import PIL.Image
import PIL.ExifTags
from sorter.extractor.gps_exception import HasntGPSData
from sorter.extractor.type_exception import NotPhotoType

class ExtractorExif:
    def __init__(self, name_file):
        if not self.is_photo(name_file):
            raise NotPhotoType

        self.photo_name = name_file
        img = PIL.Image.open(name_file)
        self.__exif = self.extractEXIF(img)

    def extractEXIF(self, img):
        try:
            exif = {
                PIL.ExifTags.TAGS[k]: v
                for k, v in img._getexif().items() if k in PIL.ExifTags.TAGS
            }
        except AttributeError:
            exif = None

        return exif

    @staticmethod
    def dms_to_dd(d, m, s, direction):
        """
        Convert dms (degree, minutes, seconds) type of coordinates to dd (Decimal Degrees)        
        """
        
        dd = float(d) + (float(m) / 60.0) + (float(s) / 3600.0)
        if direction.upper() in "SW":
            dd *= -1
        return dd

    def is_photo(self, photo_name):
        return photo_name.split('.')[-1].lower() in ['jpg']

    def transform_gps_data(self, source):
        return [val / div for val, div in source]

    def get_coordinates(self):
        """
        Returns coordinates of photo in dictionary type
        Keys:   lat, lon
        Values: float
        """

        if self.__exif is None:
            return None

        #positions in the array
        latitude = 2
        longitude = 4
        pos_cord_dir_lat = 1
        pos_cord_dir_lon = 3

        try:
            gps_data = self.__exif['GPSInfo']
        except KeyError:
            raise HasntGPSData

        cord = {
            'lat': {
                'val': self.transform_gps_data(gps_data[latitude]),
                'dir': gps_data[pos_cord_dir_lat]
            },
            'lon': {
                'val': self.transform_gps_data(gps_data[longitude]),
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

        return {'lat': lat, 'lon': lon}

    def get_date(self):
        """
        Returns the date, when the photo was created
        """
        date, time = self.__exif['DateTimeOriginal'].split(' ')
        date, time = date.split(':'), time.split(':')
        return {
            'year': date[0],
            'month': date[1],
            'day': date[2],
            'hour': time[0],
            'minute': time[1],
            'second': time[2]
        }
