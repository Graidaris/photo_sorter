#!/usr/bin/python3

from PIL import Image


class RetrieverPhotoInformation:

    def __init__(self):
        pass

    def __div_str(self, a, b):
        result = str(int(a) / int(b))
        result = result if int(result.split(
            '.')[1]) > 0 else result.split('.')[0]
        return result

    def dms_to_dd(self, d, m, s, nwse):
        dd = float(d) + (float(m) / 60.0) + (float(s) / 3600.0)
        if nwse in "SW":
            dd *= -1
        return dd

    def extract_coord(self, path):
        gps_data_exif = 34853
        latitude = 2
        longitude = 4
        pos_cord_dir_one = 1
        pos_cord_dir_two = 3

        try:
            image = Image.open(path)
            lat_coordinat = image._getexif()[gps_data_exif][latitude]
            lon_coordinat = image._getexif()[gps_data_exif][longitude]

            cardinal_direction = (
                image._getexif()[gps_data_exif][pos_cord_dir_one],
                image._getexif()[gps_data_exif][pos_cord_dir_two]
            )

        except KeyError:
            return None
        except FileNotFoundError:
            print(f"File {path} not found")
            return None
        except TypeError:
            print(f"File {path} is not subscriptable")
            return None
        except Exception as e:
            return None

        lat = ' '.join(self.__div_str(c, div) for (c, div) in lat_coordinat).split(' ')
        lon = ' '.join(self.__div_str(c, div) for (c, div) in lon_coordinat).split(' ')

        lat = self.dms_to_dd(lat[0], lat[1], lat[2], cardinal_direction[0])
        lon = self.dms_to_dd(lon[0], lon[1], lon[2], cardinal_direction[1])

        print(lat, lon)

        return (lat, cardinal_direction[0], lon, cardinal_direction[1])

    def extract_date(self, path):
        date_data_exif = 36867
        image = Image.open(path)
        date, time = image._getexif()[date_data_exif].split(' ')
        date, time = date.split(':'), time.split(':')
        return {
            'year': date[0],
            'month': date[1],
            'day': date[2],
            'hour': time[0],
            'minute': time[1],
            'second': time[2]
        }
