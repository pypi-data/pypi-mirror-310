# PythonColor | Palettes






#Imports
from random import randint
from PyColor.Colors import *






#Private Functions
def __convertFormat(targetFormat: str, current: RGB | HEX | HSV | HSL | XYZ | YCC | CMYK):
    match targetFormat:
        case 'RGB': return RGB(*current.rgb)
        case 'HEX' : return HEX(*current.hexidecimal)
        case 'HSV' : return HSV(*current.hsv)
        case 'HSL' : return HSL(*current.hsl)
        case 'XYZ' : return XYZ(*current.xyz)
        case 'YCC' : return YCC(*current.ycc)
        case 'CMYK' : return CMYK(*current.cmyk)



def __convertClassToString(Color: RGB | HEX | HSV | HSL | XYZ | YCC | CMYK):
    if type(Color) == RGB: return 'RGB'
    if type(Color) == HEX: return 'HEX'
    if type(Color) == HSV: return 'HSV'
    if type(Color) == HSL: return 'HSL'
    if type(Color) == XYZ: return 'XYZ'
    if type(Color) == YCC: return 'YCC'
    if type(Color) == CMYK: return 'CMYK'



def __capNumber(cap: int, number: int):
    if number < 0: return number + cap
    if number > cap: return number - cap
    return number




#Public Functions
def GeneratePalette(Color: RGB | HEX | HSV | HSL | XYZ | YCC | CMYK, scheme: str) -> list:
    """
    Function to generate a color pallete given a Color class object and a scheme.

    Attributes:
        Color (RGB | HEX | HSV | HSL | XYZ | YCC | CMYK): Color to generate pallete from.
        scheme (str): Scheme to use for the pallete, must be one of the supported schemes.

    
    Suported Schemes:
     - monochromatic
     - analogous
     - complimentary
     - splitcomplimentary
     - tetradic
     - triad
     - random
    """
    
    if type(Color) not in [RGB, HEX, HSV, HSL, XYZ, YCC, CMYK]: return 'Invalid Color Type'
    if scheme not in ['monochromatic', 'analogous', 'complimentary', 'splitcomplimentary', 'tetrad', 'triad', 'random']: return 'Invalid Scheme Provided'


    match scheme:
        case 'monochromatic':
            hue = Color.hsv[0]
            saturation = Color.hsv[1]
            Values = [__capNumber(100, Color.hsv[2] - 45), Color.hsv[2], __capNumber(100, Color.hsv[2] + 45)]

            return [__convertFormat(__convertClassToString(Color), HSV(hue, saturation, value)) for value in Values]
            
            
        case 'analogous':
            Hues = [__capNumber(360, Color.hsv[0] - 30), Color.hsv[0], __capNumber(360, Color.hsv[0] + 30)]
            saturation = Color.hsv[1]
            value = Color.hsv[2]

            return [__convertFormat(__convertClassToString(Color), HSV(hue, saturation, value)) for hue in Hues]


        case 'complimentary':
            Hues = [__capNumber(360, Color.hsv[0] - 180), Color.hsv[0]]
            saturation = Color.hsv[1]
            value = Color.hsv[2]

            return [__convertFormat(__convertClassToString(Color), HSV(hue, saturation, value)) for hue in Hues]
        

        case 'splitcomplimentary':
            Hues = [__capNumber(360, Color.hsv[0] - 150), __capNumber(360, Color.hsv[0] - 210), Color.hsv[0]]
            saturation = Color.hsv[1]
            value = Color.hsv[2]

            return [__convertFormat(__convertClassToString(Color), HSV(hue, saturation, value)) for hue in Hues]


        case 'tetrad':
            Hues = [__capNumber(360, Color.hsv[0] + (45 * (i + 1))) for i in range(3)] + [Color.hsv[0]]
            saturation = Color.hsv[1]
            value = Color.hsv[2]

            return [__convertFormat(__convertClassToString(Color), HSV(hue, saturation, value)) for hue in Hues]


        case 'triad':
            Hues = [__capNumber(360, Color.hsv[0] - 120), Color.hsv[0], __capNumber(360, Color.hsv[0] + 120)]
            saturation = Color.hsv[1]
            value = Color.hsv[2]

            return [__convertFormat(__convertClassToString(Color), HSV(hue, saturation, value)) for hue in Hues]
        

        case 'random':
            Hues = [__capNumber(360, Color.hsv[0] + randint(-360, 360)) for i in range(3)] + [Color.hsv[0]]
            saturation = Color.hsv[1]
            value = Color.hsv[2]

            return [__convertFormat(__convertClassToString(Color), HSV(hue, saturation, value)) for hue in Hues]