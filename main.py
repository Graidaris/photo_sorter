from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

im = Image.open('test3.jpg')
n_coordinat = im._getexif()[34853][2]
e_coordinat = im._getexif()[34853][4]

def div_str(a, b):
    dividend = int(a)
    divider = int(b)
    result = str(dividend/divider)
    result = result if int(result.split('.')[1]) > 0 else result.split('.')[0]
    return result
    

cor_n = ' '.join(div_str(c, div) for (c, div) in n_coordinat)
cor_e = ' '.join(div_str(c, div) for (c, div) in e_coordinat)


print(cor_n,'N',cor_e,'E')