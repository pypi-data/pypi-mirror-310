# PyColor | Functions






#Imports
from Colors import *






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




#Public Functions
def Interpolate(ColorList: list[RGB, HEX, HSV, HSL, XYZ, YCC, CMYK]) -> list:
    NewColorList = [color.rgb for color in ColorList] + [(0, 0, 0)]
    NewColorList = [[RGB(*NewColorList[i]), RGB(*[int(round((NewColorList[i][c] + NewColorList[i + 1][c]) / 2.0)) for c in range(3)])] for i in range(len(NewColorList) - 1)]
    return [color for colorset in NewColorList for color in colorset][:-1]



def InterpolateFormat(ColorList: list[RGB, HEX, HSV, HSL, XYZ, YCC, CMYK]) -> list:
    NewColorList = Interpolate(ColorList)
    return [__convertFormat(__convertClassToString(ColorList[0]), color) for color in NewColorList]