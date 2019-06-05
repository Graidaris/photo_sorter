#!/usr/bin/python3

import PIL.Image
import PIL.ExifTags


class RetrieverPhotoInformation:

    def __init__(self, name_file):
        img = PIL.Image.open(name_file)
        self.exif = {
            PIL.ExifTags.TAGS[k]: v
            for k, v in img._getexif().items()
            if k in PIL.ExifTags.TAGS
        }

    @staticmethod
    def dms_to_dd(d, m, s, direction):
        dd = float(d) + (float(m) / 60.0) + (float(s) / 3600.0)
        if direction.upper() in "SW":
            dd *= -1
        return dd

    def __transform_gps_data(self, source):
        return [val/div for val, div in source]

    def get_coordinates(self):
        latitude = 2
        longitude = 4
        pos_cord_dir_lat = 1
        pos_cord_dir_lon = 3

        gps_data = self.exif['GPSInfo']

        cord = {
            'lat': {'val': self.__transform_gps_data(gps_data[latitude]),
                    'dir': gps_data[pos_cord_dir_lat]
                    },

            'lon': {'val': self.__transform_gps_data(gps_data[longitude]),
                    'dir': gps_data[pos_cord_dir_lon]
                    }
        }

        lat = self.dms_to_dd(cord['lat']['val'][0], cord['lat']['val'][1], cord['lat']['val'][2], cord['lat']['dir'])
        lon = self.dms_to_dd(cord['lon']['val'][0], cord['lon']['val'][1], cord['lon']['val'][2], cord['lon']['dir'])

        return {
            'lat': lat,
            'lon': lon
                }

    def extract_date(self):
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
