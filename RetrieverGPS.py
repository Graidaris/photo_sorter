from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


class RetrieverGPS:

    def __init__(self):
        pass

    def div_str(self, a, b):
        dividend = int(a)
        divider = int(b)
        result = str(dividend/divider)
        result = result if int(result.split(
            '.')[1]) > 0 else result.split('.')[0]
        return result

    def extract_coord(self, path):
        gps_data_exif_IOS = 34853
        latitude = 2
        longitude = 4
        pos_cord_dir_one = 1
        pos_cord_dir_two = 3        
        
        try:
            image = Image.open(path)
            n_coordinat = image._getexif()[gps_data_exif_IOS][latitude]
            e_coordinat = image._getexif()[gps_data_exif_IOS][longitude]

            cardinal_direction = (
                image._getexif()[gps_data_exif_IOS][pos_cord_dir_one],
                image._getexif()[gps_data_exif_IOS][pos_cord_dir_two]
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

        cor_n = ' '.join(self.div_str(c, div) for (c, div) in n_coordinat)
        cor_e = ' '.join(self.div_str(c, div) for (c, div) in e_coordinat)

        return (cor_n, cardinal_direction[0], cor_e, cardinal_direction[1])
