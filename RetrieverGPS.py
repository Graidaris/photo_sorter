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
        image = Image.open(path)
        try:
            n_coordinat = image._getexif()[34853][2]
            e_coordinat = image._getexif()[34853][4]
        except KeyError:
            return None
        except Exception:
            return None

        cor_n = ' '.join(self.div_str(c, div) for (c, div) in n_coordinat)
        cor_e = ' '.join(self.div_str(c, div) for (c, div) in e_coordinat)

        return (cor_n, 'N', cor_e, 'E')
