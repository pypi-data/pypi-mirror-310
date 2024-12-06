# PythonColor | Color






#Imports
from math import degrees, acos, sqrt






#Classes
class RGB:
    """
    RGB color class object. 
    Takes in a red, green, and blue value between 0-255

    Attributes:
        red (int): An integer value between 0-255 or float value between 0-1.
        green (int): An integer value between 0-255 or float value between 0-1.
        blue (int): An integer value between 0-255 or float value between 0-1.

    Valid Examples:
     - RGB(100, 100, 100)
     - RGB(30, 30, 30)
     - RGB(50, 34, 200)

    Invalid Examples:
     - RGB(234, 300, 100)
     - RGB(249, 29, 290)
     - RGB(365, 265, 100)
    """
    
    @staticmethod
    def __checkIfValid(value):
        if any([True for i in value if type(i) not in [int, float]]): return False
        value = [int(i * 255) if type(i) == float else int(i) for i in value]
        if len([i for i in value if i >= 0 and i <= 256]) != 3: return False

        return True



    def __init__(self, red: int | float, green: int | float, blue: int | float, notPercent: bool = False):
        if self.__checkIfValid((red, green, blue)):
            if not notPercent:
                if type(red) == float: red = int(red * 255)
                if type(green) == float: green = int(green * 255)
                if type(blue) == float: blue = int(blue * 255)

            self.red = red
            self.green = green
            self.blue = blue
            self.__valid = True
        
        else: self.__valid = False
    

    @property
    def rgb(self) -> tuple:
        if not self.__valid: return None
        return (self.red, self.green, self.blue)


    @property
    def hexidecimal(self) -> str:
        if not self.__valid: return None

        r = hex(self.red)[2:].zfill(2).upper()
        g = hex(self.green)[2:].zfill(2).upper()
        b = hex(self.blue)[2:].zfill(2).upper()

        return '#' + ''.join([r, g, b])


    @property
    def hsv(self) -> tuple:
        if not self.__valid: return None

        M = max(self.red, self.green, self.blue)
        m = min(self.red, self.green, self.blue)

        V = (M / 255) * 100

        S = 0
        if M > 0: S = 100 - ((m / M) * 100)

        try:
            H = degrees(acos((self.red - (self.green / 2) - (self.blue / 2)) / sqrt((self.red ** 2) + (self.green ** 2) + (self.blue ** 2) - (self.red * self.green) - (self.red * self.blue) - (self.green * self.blue))))
            if self.blue > self.green: H = 360 - H
        except: H = 0

        H = int(round(H))
        S = int(round(S))
        V = int(round(V))

        return (H, S, V)


    @property 
    def hsl(self) -> tuple:
        if not self.__valid: return None

        M = max([self.red, self.green, self.blue])
        m = min([self.red, self.green, self.blue])

        M = max([(self.red / 255.0), (self.green / 255.0), (self.blue / 255.0)])
        m = min([(self.red / 255.0), (self.green / 255.0), (self.blue / 255.0)])

        C = M - m
        L = (M + m) / 2.0

        S = 0
        if C != 0: S = ((C / (1.0 - abs((2.0 * L) - 1.0))) * 100.0)
		
        try:
            H = degrees(acos((self.red - (self.green / 2) - (self.blue / 2)) / sqrt((self.red ** 2) + (self.green ** 2) + (self.blue ** 2) - (self.red * self.green) - (self.red * self.blue) - (self.green * self.blue))))
            if self.blue > self.green: H = 360 - H
        except: H = 0

        H = int(round(H))
        S = int(round(S))
        L = int(round(L * 100.0))
			
        return (H, S, L)
    

    @property
    def xyz(self) -> tuple:
        if not self.__valid: return None

        r = self.red / 255.0
        g = self.green / 255.0
        b = self.blue / 255.0

        rgb = [(((i + 0.055) / 1.055) ** 2.4) if i > 0.04045 else (i / 12.92) for i in [r, g, b]]

        x = round((rgb[0] * 41.24 + rgb[1] * 35.76 + rgb[2] * 18.05), 2)
        y = round((rgb[0] * 21.26 + rgb[1] * 71.52 + rgb[2] * 7.22), 2)
        z = round((rgb[0] * 1.93 + rgb[1] * 11.92 + rgb[2] * 95.05), 2)

        return (x, y, z)

      
    @property
    def ycc(self) -> tuple:
        if not self.__valid: return None

        y = round((16 + ((65.738 * self.red) / 256) + ((129.057 * self.green) / 256) + ((25.064 * self.blue) / 256)), 2)
        cb = round((128 - ((37.945 * self.red) / 256) - ((74.494 * self.green) / 256) + ((112.439 * self.blue) / 256)), 2)
        cr = round((128 + ((112.439 * self.red) / 256) - ((94.154 * self.green) / 256) - ((18.285 * self.blue) / 256)), 2)

        return (y, cb, cr)


    @property
    def cmyk(self) -> str:
        if not self.__valid: return None

        nr = self.red / 255.0
        ng = self.green / 255.0
        nb = self.blue / 255.0

        K = 1.0 - max(nr, ng, nb)

        C = int(round(((1 - nr - K) / (1 - K) * 100)))
        M = int(round(((1 - ng - K) / (1 - K) * 100)))
        Y = int(round(((1 - nb - K) / (1 - K) * 100)))
        K = int(round(K * 100))

        return (C, M, Y, K)
    

    @property
    def percentForm(self) -> tuple:
        if not self.__valid: return None

        r = round((self.red / 255.0), 2)
        g = round((self.green / 255.0), 2)
        b = round((self.blue / 255.0), 2)

        return (r, g, b)
    

    @property
    def grayscale(self) -> tuple:
        if not self.__valid: return None

        gv = int(round((self.red + self.green + self.blue) / 3.0))

        return RGB(gv, gv, gv)


    @property
    def greyscale(self) -> tuple: return self.grayscale
        


    def __repr__(self):
        if not self.__valid: return 'Invalid RGB'
        return str(self.red) + ' ' + str(self.green) + ' ' + str(self.blue)




class HEX:
    """
    HEX color class object. 
    Takes in a hexidecimal representation of a color as a string that includes the #.

    Attributes:
        hexicode (str): A hexidecimal form of a color.

    Valid Examples:
     - HEX("#121212")
     - HEX("#A32B12")
     - HEX("#FEFF73")

    Invalid Examples:
     - HEX(121212)
     - HEX("A3312")
     - HEX("311252")
    """

    @staticmethod
    def __checkIfValid(value):
        if type(value) != str: return False
        value = [value[1:][i:i+2] for i in range(0, len(value[1:]), 2)]

        if any([True for i in value if len(i) != 2]): return False

        try: value = [int(i, 16) for i in value]
        except: return False

        if any([True for i in value if i > 255]) or any([True for i in value if i < 0]): return False

        return True



    def __init__(self, hexicode: str):
        if self.__checkIfValid(hexicode):
            self.hexicode = hexicode
            self.__valid = True
        
        else: self.__valid = False
    

    @property
    def rgb(self) -> tuple:
        if not self.__valid: return None

        Values = [self.Values[1:][i:i+2] for i in range(0, len(self.Values[1:]), 2)]
        Values = [int(i, 16) for i in Values]

        return tuple(Values)


    @property
    def hexidecimal(self) -> str:
        if not self.__valid: return None
        return self.hexicode
    

    @property
    def hsv(self) -> tuple:
        if not self.__valid: return None

        M = max(self.rgb[0], self.rgb[1], self.rgb[2])
        m = min(self.rgb[0], self.rgb[1], self.rgb[2])

        V = (M / 255) * 100

        S = 0
        if M > 0: S = 100 - ((m / M) * 100)

        try:
            H = degrees(acos((self.rgb[0] - (self.rgb[1] / 2) - (self.rgb[2] / 2)) / sqrt((self.rgb[0] ** 2) + (self.rgb[1] ** 2) + (self.rgb[2] ** 2) - (self.rgb[0] * self.rgb[1]) - (self.red * self.rgb[2]) - (self.rgb[1] * self.rgb[2]))))
            if self.rgb[2] > self.rgb[1]: H = 360 - H
        except: H = 0

        H = int(round(H))
        S = int(round(S))
        V = int(round(V))

        return (H, S, V)
    

    @property 
    def hsl(self) -> tuple:
        if not self.__valid: return None

        M = max([self.rgb[0], self.rgb[1], self.rgb[2]])
        m = min([self.rgb[0], self.rgb[1], self.rgb[2]])

        M = max([(self.rgb[0] / 255.0), (self.rgb[1] / 255.0), (self.rgb[2] / 255.0)])
        m = min([(self.rgb[0] / 255.0), (self.rgb[1] / 255.0), (self.rgb[2] / 255.0)])

        C = M - m
        L = (M + m) / 2.0

        S = 0
        if C != 0: S = ((C / (1.0 - abs((2.0 * L) - 1.0))) * 100.0)
		
        try:
            H = degrees(acos((self.rgb[0] - (self.rgb[1] / 2) - (self.rgb[2] / 2)) / sqrt((self.rgb[0] ** 2) + (self.rgb[1] ** 2) + (self.rgb[2] ** 2) - (self.rgb[0] * self.rgb[1]) - (self.rgb[0] * self.rgb[2]) - (self.rgb[1] * self.rgb[2]))))
            if self.rgb[2] > self.rgb[1]: H = 360 - H
        except: H = 0

        H = int(round(H))
        S = int(round(S))
        L = int(round(L * 100.0))
			
        return (H, S, L)
    

    @property
    def xyz(self) -> tuple:
        if not self.__valid: return None

        r = self.rgb[0] / 255.0
        g = self.rgb[1] / 255.0
        b = self.rgb[2] / 255.0

        rgb = [(((i + 0.055) / 1.055) ** 2.4) if i > 0.04045 else (i / 12.92) for i in [r, g, b]]

        x = round((rgb[0] * 41.24 + rgb[1] * 35.76 + rgb[2] * 18.05), 2)
        y = round((rgb[0] * 21.26 + rgb[1] * 71.52 + rgb[2] * 7.22), 2)
        z = round((rgb[0] * 1.93 + rgb[1] * 11.92 + rgb[2] * 95.05), 2)

        return (x, y, z)

      
    @property
    def ycc(self) -> tuple:
        if not self.__valid: return None

        y = round((16 + ((65.738 * self.rgb[0]) / 256) + ((129.057 * self.rgb[1]) / 256) + ((25.064 * self.rgb[2]) / 256)), 2)
        cb = round((128 - ((37.945 * self.rgb[0]) / 256) - ((74.494 * self.rgb[1]) / 256) + ((112.439 * self.rgb[2]) / 256)), 2)
        cr = round((128 + ((112.439 * self.rgb[0]) / 256) - ((94.154 * self.rgb[1]) / 256) - ((18.285 * self.rgb[2]) / 256)), 2)

        return (y, cb, cr)
      

    @property
    def cmyk(self):
        if not self.__valid: return None

        nr = self.rgb[0] / 255.0
        ng = self.rgb[1] / 255.0
        nb = self.rgb[2] / 255.0

        K = 1.0 - max(nr, ng, nb)

        C = int(round(((1 - nr - K) / (1 - K) * 100)))
        M = int(round(((1 - ng - K) / (1 - K) * 100)))
        Y = int(round(((1 - nb - K) / (1 - K) * 100)))
        K = int(round(K * 100))

        return (C, M, Y, K)


    @property
    def percentForm(self) -> float:
        Numbers = [int(i, 16) for i in self.hexicode[1:]][::-1]
        Numbers = [((16 ** i) * Numbers[i]) for i in range(len(Numbers))]

        number = sum(Numbers)

        return round((number / 16777215.0), 3)
    

    @property
    def grayscale(self) -> tuple:
        if not self.__valid: return None

        gv = int(round((self.rgb[0] + self.rgb[1] + self.rgb[2]) / 3.0))
        rgbGray = RGB(gv, gv, gv)

        return HEX(rgbGray.hexidecimal)
    

    @property
    def greyscale(self) -> tuple: return self.grayscale
    


    def __repr__(self):
        if not self.__valid: return 'Invalid HEX'
        return self.hexicode




class HSV:
    """
    HSV color class object. 
    Takes in hue, saturation, and value values.

    Attributes:
        hue (int | float): An integer value between 0-360 or float value between 0-1.
        saturation (int | float): An integer value between 0-100 or float value between 0-1.
        value (int | float): An integer value between 0-100 or float value between 0-1.

        
    Valid Examples:
     - HSV(342, 100, 100)
     - HSV(100, 30, 80)
     - HSV(50, 30, 100)

    Invalid Examples:
     - HSV(2, 101, 50)
     - HSV(-3, 29, 290)
     - HSV(365, 123, 100)
    """
    
    @staticmethod
    def __checkIfValid(value):
        if any([True for i in value if type(i) not in [int, float]]): return False
        value = list(value)

        if type(value[0]) == float: value[0] *= 360
        if type(value[1]) == float: value[1] *= 100
        if type(value[2]) == float: value[2] *= 100

        if value[0] < 0 or value[0] > 360: return False
        if value[1] < 0 or value[1] > 100: return False
        if value[2] < 0 or value[2] > 100: return False

        return True



    def __init__(self, hue: int | float, saturation: int | float, value: int | float, notPercent: bool = False):
        if self.__checkIfValid((hue, saturation, value)):
            if not notPercent:
                if type(hue) == float: hue = int(hue * 360)
                if type(saturation) == float: saturation = int(saturation * 100)
                if type(value) == float: value = int(value * 100)

            self.hue = hue
            self.saturation = saturation
            self.value = value
            self.__valid = True
        
        else: self.__valid = False
    

    @property
    def rgb(self) -> tuple:
        if not self.__valid: return None

        value = self.value / 100.0
        saturation = self.saturation / 100.0
		
        C = value * saturation
        X = C * (1.0 - abs(((self.hue / 60.0) % 2.0) - 1.0))
        m = value - C
		
        match int(self.hue / 60.0):
            case 0: rgb = [C, X, 0]
            case 1: rgb = [X, C, 0]
            case 2: rgb = [0, C, X]
            case 3: rgb = [0, X, C]
            case 4: rgb = [X, 0, C]
            case 5 | 6: rgb = [C, 0, X]
        
        rgb = [((rgb[0] + m) * 255.0), ((rgb[1] + m) * 255.0), ((rgb[2] + m) * 255.0)]
        rgb = [int(round(i)) for i in rgb]

        return (rgb[0], rgb[1], rgb[2])
    

    @property
    def hexidecimal(self) -> str:
        if not self.__valid: return None

        r = hex(self.rgb[0])[2:].zfill(2).upper()
        g = hex(self.rgb[1])[2:].zfill(2).upper()
        b = hex(self.rgb[2])[2:].zfill(2).upper()

        return '#' + ''.join([r, g, b])
    

    @property
    def hsv(self) -> tuple:
        return (self.hue, self.saturation, self.value)
        

    @property
    def hsl(self) -> tuple:
        if not self.__valid: return None

        s = self.saturation / 100.0
        v = self.value / 100.0

        L = (2 - s) * v / 2.0

        if L != 0:
            if L == 1: S = 0
            elif L < 0.5: S = int(round(s * v / (L * 2.0)))
            else: S = int(round(s * v / (2.0 - L * 2.0)))
        
        S = int(round(S * 100.0))
        L = int(round(L * 100.0))

        return (self.hue, S, L)
    

    @property
    def xyz(self) -> tuple:
        if not self.__valid: return None

        r = self.rgb[0] / 255.0
        g = self.rgb[1] / 255.0
        b = self.rgb[2] / 255.0

        rgb = [(((i + 0.055) / 1.055) ** 2.4) if i > 0.04045 else (i / 12.92) for i in [r, g, b]]

        x = round((rgb[0] * 41.24 + rgb[1] * 35.76 + rgb[2] * 18.05), 2)
        y = round((rgb[0] * 21.26 + rgb[1] * 71.52 + rgb[2] * 7.22), 2)
        z = round((rgb[0] * 1.93 + rgb[1] * 11.92 + rgb[2] * 95.05), 2)

        return (x, y, z)
    

    @property
    def ycc(self) -> tuple:
        if not self.__valid: return None

        y = round((16 + ((65.738 * self.rgb[0]) / 256) + ((129.057 * self.rgb[1]) / 256) + ((25.064 * self.rgb[2]) / 256)), 2)
        cb = round((128 - ((37.945 * self.rgb[0]) / 256) - ((74.494 * self.rgb[1]) / 256) + ((112.439 * self.rgb[2]) / 256)), 2)
        cr = round((128 + ((112.439 * self.rgb[0]) / 256) - ((94.154 * self.rgb[1]) / 256) - ((18.285 * self.rgb[2]) / 256)), 2)

        return (y, cb, cr)
    

    @property
    def cmyk(self) -> tuple:
        if not self.__valid: return None

        nr = self.rgb[0] / 255.0
        ng = self.rgb[1] / 255.0
        nb = self.rgb[2] / 255.0

        K = 1.0 - max(nr, ng, nb)

        C = int(round(((1 - nr - K) / (1 - K) * 100)))
        M = int(round(((1 - ng - K) / (1 - K) * 100)))
        Y = int(round(((1 - nb - K) / (1 - K) * 100)))
        K = int(round(K * 100))

        return (C, M, Y, K)
    

    @property
    def percentForm(self) -> tuple:
        if not self.__valid: return None

        h = round((self.hue / 360.0), 2)
        s = round((self.saturation / 100.0), 2)
        v = round((self.value / 100.0), 2)

        return (h, s, v)
    

    @property
    def grayscale(self) -> tuple:
        if not self.__valid: return None

        gv = int(round((self.rgb[0] + self.rgb[1] + self.rgb[2]) / 3.0))
        rgbGray = RGB(gv, gv, gv)

        return HSV(*rgbGray.hsv)
    

    @property
    def greyscale(self) -> tuple: return self.grayscale
    


    def __repr__(self):
        if not self.__valid: return 'Invalid HSV'
        return str(self.hue) + '° ' + str(self.saturation) + '% ' + str(self.value) + '%'




class HSL:
    """
    HSL color class object. 
    Takes in hue, saturation, and lightness values.

    Attributes:
        hue (int | float): An integer value between 0-360 or float value between 0-1.
        saturation (int | float): An integer value between 0-100 or float value between 0-1.
        lightness (int | float): An integer value between 0-100 or float value between 0-1.

        
    Valid Examples:
     - HSL(342, 100, 100)
     - HSL(100, 30, 80)
     - HSL(50, 30, 100)

    Invalid Examples:
     - HSL(2, 101, 50)
     - HSL(-3, 29, 290)
     - HSL(365, 123, 100)
    """

    @staticmethod
    def __checkIfValid(value):
        if any([True for i in value if type(i) not in [int, float]]): return False
        value = list(value)

        if type(value[0]) == float: value[0] *= 360
        if type(value[1]) == float: value[1] *= 100
        if type(value[2]) == float: value[2] *= 100

        if value[0] < 0 or value[0] > 360: return False
        if value[1] < 0 or value[1] > 100: return False
        if value[2] < 0 or value[2] > 100: return False

        return True



    def __init__(self, hue: int | float, saturation: int | float, lightness: int | float, notPercent: bool = False):
        if self.__checkIfValid((hue, saturation, lightness)):
            if not notPercent:
                if type(hue) == float: hue = int(hue * 360)
                if type(saturation) == float: saturation = int(saturation * 100)
                if type(lightness) == float: lightness = int(lightness * 100)

            self.hue = hue
            self.saturation = saturation
            self.lightness = lightness
            self.__valid = True
        
        else: self.__valid = False
    

    @property
    def rgb(self) -> tuple:
        if not self.__valid: return None

        saturation = self.saturation / 100
        lightness = self.lightness / 100
		
        C = (1 - abs((2 * lightness) - 1)) * saturation
		
        X = C * (1 - abs(((self.hue / 60) % 2) - 1))
		
        m = lightness - (C / 2)

        match int(self.hue / 60.0):
            case 0: rgb = [C, X, 0]
            case 1: rgb = [X, C, 0]
            case 2: rgb = [0, C, X]
            case 3: rgb = [0, X, C]
            case 4: rgb = [X, 0, C]
            case 5 | 6: rgb = [C, 0, X]
		
		
        rgb = [((rgb[0] + m) * 255), ((rgb[1] + m) * 255), ((rgb[2] + m) * 255)]
        rgb = [int(round(i)) for i in rgb]
			
        return (rgb[0], rgb[1], rgb[2])


    @property
    def hexidecimal(self) -> str:
        if not self.__valid: return None

        r = hex(self.rgb[0])[2:].zfill(2).upper()
        g = hex(self.rgb[1])[2:].zfill(2).upper()
        b = hex(self.rgb[2])[2:].zfill(2).upper()

        return '#' + ''.join([r, g, b])
    

    @property
    def hsv(self) -> tuple:
        if not self.__valid: return None

        L = (self.lightness / 100.0) * 2

        if L <= 1: S = (self.saturation / 100.0) * L
        else: S = 2 - L

        S = int(round((2.0 * S) / (L + S)))
        V = int(round((L + S) / 2.0))

        return (self.hue, S, V)


    @property
    def hsl(self) -> tuple:
        if not self.__valid: return None
        return (self.hue, self.saturation, self.lightness)
    

    @property
    def xyz(self) -> tuple:
        if not self.__valid: return None

        r = self.rgb[0] / 255.0
        g = self.rgb[1] / 255.0
        b = self.rgb[2] / 255.0

        rgb = [(((i + 0.055) / 1.055) ** 2.4) if i > 0.04045 else (i / 12.92) for i in [r, g, b]]

        x = round((rgb[0] * 41.24 + rgb[1] * 35.76 + rgb[2] * 18.05), 2)
        y = round((rgb[0] * 21.26 + rgb[1] * 71.52 + rgb[2] * 7.22), 2)
        z = round((rgb[0] * 1.93 + rgb[1] * 11.92 + rgb[2] * 95.05), 2)

        return (x, y, z)
    

    @property
    def ycc(self) -> tuple:
        if not self.__valid: return None

        y = round((16 + ((65.738 * self.rgb[0]) / 256) + ((129.057 * self.rgb[1]) / 256) + ((25.064 * self.rgb[2]) / 256)), 2)
        cb = round((128 - ((37.945 * self.rgb[0]) / 256) - ((74.494 * self.rgb[1]) / 256) + ((112.439 * self.rgb[2]) / 256)), 2)
        cr = round((128 + ((112.439 * self.rgb[0]) / 256) - ((94.154 * self.rgb[1]) / 256) - ((18.285 * self.rgb[2]) / 256)), 2)

        return (y, cb, cr)
    

    @property
    def cmyk(self) -> tuple:
        if not self.__valid: return None

        nr = self.rgb[0] / 255.0
        ng = self.rgb[1] / 255.0
        nb = self.rgb[2] / 255.0

        K = 1.0 - max(nr, ng, nb)

        C = int(round(((1 - nr - K) / (1 - K) * 100)))
        M = int(round(((1 - ng - K) / (1 - K) * 100)))
        Y = int(round(((1 - nb - K) / (1 - K) * 100)))
        K = int(round(K * 100))

        return (C, M, Y, K)
    

    @property
    def percentForm(self) -> tuple:
        if not self.__valid: return None

        h = round((self.hue / 360.0), 2)
        s = round((self.saturation / 100.0), 2)
        l = round((self.lightness / 100.0), 2)

        return (h, s, l)
    

    @property
    def grayscale(self) -> tuple:
        if not self.__valid: return None

        gv = int(round((self.rgb[0] + self.rgb[1] + self.rgb[2]) / 3.0))
        rgbGray = RGB(gv, gv, gv)

        return HSL(*rgbGray.hsl)
    

    @property
    def greyscale(self) -> tuple: return self.grayscale
    


    def __repr__(self):
        if not self.__valid: return 'Invalid HSL'
        return str(self.hue) + '° ' + str(self.saturation) + '% ' + str(self.lightness) + '%'




class XYZ:
    """
    XYZ color class object. 
    Takes in cyan, magenta, yellow, and key values.

    Attributes:
        x (float): A float value between 0-95.05 or 0-1.
        y (float): A float value between 0-100.0 or 0-1.
        z (float): A float value between 0-108.9 or 0-1.

        
    Valid Examples:
     - XYZ(84.0, 100.0, 102.0)
     - XYZ(1.0, 30.0, 106.5)
     - XYZ(53.7, 23.4, 100.0)

    Invalid Examples:
     - XYZ(100.0, 101.3, 12.7)
     - XYZ(-3, 29.0, 290.3)
     - XYZ(-13.2, 113.0, 100.0)
    """


    @staticmethod
    def __checkIfValid(value):
        try: value = [float(i) for i in value if type(i) in [int, float]]
        except: return False

        if len(value) != 3: return False
        if any([True for i in value if i < 0]): return False
        if value[0] > 95.05 or value[1] > 100 or value[2] > 108.9: return False

        return True


        
    def __init__(self, x: float, y: float, z: float, notPercent: bool = False):
        if self.__checkIfValid((x, y, z)):
            if all([True if i >= 0 and i <= 1 else False for i in (x, y, z)]) and not notPercent:
                self.x = round((x * 95.05), 2)
                self.y = round((y * 100.0), 2)
                self.z = round((z * 108.9), 2)
            
            else:
                self.x = round(x, 2)
                self.y = round(y, 2)
                self.z = round(z, 2)
            
            self.__valid = True
        
        else: self.__valid = False         


    @property
    def rgb(self) -> tuple:
        if not self.__valid: return None

        r = self.x * 0.032406 - self.y * 0.015372 - self.z * 0.004986
        g = self.x * -0.009689 + self.y * 0.018758 + self.z * 0.000415
        b = self.x * 0.000557 - self.y * 0.00204 + self.z * 0.01057

        rgb = [(1.055 * (i ** 0.4167) - 0.055) if i > 0.0031308 else (i * 12.92) for i in [r, g, b]]

        r = int(round(rgb[0] * 255))
        g = int(round(rgb[1] * 255))
        b = int(round(rgb[2] * 255))

        return (r, g, b)
    

    @property
    def hexidecimal(self) -> str:
        if not self.__valid: return None

        r = hex(self.rgb[0])[2:].zfill(2).upper()
        g = hex(self.rgb[1])[2:].zfill(2).upper()
        b = hex(self.rgb[2])[2:].zfill(2).upper()

        return '#' + ''.join([r, g, b])
    

    @property
    def hsv(self) -> tuple:
        if not self.__valid: return None

        M = max(self.rgb[0], self.rgb[1], self.rgb[2])
        m = min(self.rgb[0], self.rgb[1], self.rgb[2])

        V = (M / 255) * 100

        S = 0
        if M > 0: S = 100 - ((m / M) * 100)

        try:
            H = degrees(acos((self.rgb[0] - (self.rgb[1] / 2) - (self.rgb[2] / 2)) / sqrt((self.rgb[0] ** 2) + (self.rgb[1] ** 2) + (self.rgb[2] ** 2) - (self.rgb[0] * self.rgb[1]) - (self.red * self.rgb[2]) - (self.rgb[1] * self.rgb[2]))))
            if self.rgb[2] > self.rgb[1]: H = 360 - H
        except: H = 0

        H = int(round(H))
        S = int(round(S))
        V = int(round(V))

        return (H, S, V)
    

    @property 
    def hsl(self) -> tuple:
        if not self.__valid: return None

        M = max([self.rgb[0], self.rgb[1], self.rgb[2]])
        m = min([self.rgb[0], self.rgb[1], self.rgb[2]])

        M = max([(self.rgb[0] / 255.0), (self.rgb[1] / 255.0), (self.rgb[2] / 255.0)])
        m = min([(self.rgb[0] / 255.0), (self.rgb[1] / 255.0), (self.rgb[2] / 255.0)])

        C = M - m
        L = (M + m) / 2.0

        S = 0
        if C != 0: S = ((C / (1.0 - abs((2.0 * L) - 1.0))) * 100.0)
		
        try:
            H = degrees(acos((self.rgb[0] - (self.rgb[1] / 2) - (self.rgb[2] / 2)) / sqrt((self.rgb[0] ** 2) + (self.rgb[1] ** 2) + (self.rgb[2] ** 2) - (self.rgb[0] * self.rgb[1]) - (self.rgb[0] * self.rgb[2]) - (self.rgb[1] * self.rgb[2]))))
            if self.rgb[2] > self.rgb[1]: H = 360 - H
        except: H = 0

        H = int(round(H))
        S = int(round(S))
        L = int(round(L * 100.0))
			
        return (H, S, L)
    

    @property
    def xyz(self) -> tuple:
        if not self.__valid: return None
        return (self.x, self.y, self.z)
    

    @property
    def ycc(self) -> tuple:
        if not self.__valid: return None

        y = round((16 + ((65.738 * self.rgb[0]) / 256) + ((129.057 * self.rgb[1]) / 256) + ((25.064 * self.rgb[2]) / 256)), 2)
        cb = round((128 - ((37.945 * self.rgb[0]) / 256) - ((74.494 * self.rgb[1]) / 256) + ((112.439 * self.rgb[2]) / 256)), 2)
        cr = round((128 + ((112.439 * self.rgb[0]) / 256) - ((94.154 * self.rgb[1]) / 256) - ((18.285 * self.rgb[2]) / 256)), 2)

        return (y, cb, cr)
    

    @property
    def cmyk(self):
        if not self.__valid: return None

        nr = self.rgb[0] / 255.0
        ng = self.rgb[1] / 255.0
        nb = self.rgb[2] / 255.0

        K = 1.0 - max(nr, ng, nb)

        C = int(round(((1 - nr - K) / (1 - K) * 100)))
        M = int(round(((1 - ng - K) / (1 - K) * 100)))
        Y = int(round(((1 - nb - K) / (1 - K) * 100)))
        K = int(round(K * 100))

        return (C, M, Y, K)


    @property
    def percentForm(self) -> float:
        x = round((self.x / 95.05), 2)
        y = round((self.y / 100.0), 2)
        z = round((self.z / 108.9), 2)

        return (x, y, z)
    

    @property
    def grayscale(self) -> tuple:
        if not self.__valid: return None

        gv = int(round((self.rgb[0] + self.rgb[1] + self.rgb[2]) / 3.0))
        rgbGray = RGB(gv, gv, gv)

        return XYZ(*rgbGray.xyz)
    

    @property
    def greyscale(self) -> tuple: return self.grayscale



    def __repr__(self):
        if not self.__valid: return 'Invalid XYZ'
        return str(self.x) + '% ' + str(self.y) + '% ' + str(self.z) + '%'




class YCC:
    """
    CMYK color class object. 
    Takes in cyan, magenta, yellow, and key values.

    Attributes:
        y (float): An float value between 0-255 or 0-1.
        cb (float): An float value between 0-255 or 0-1.
        cr (float): An float value between 0-255 or 0-1.
        
  
    Valid Examples:
     - YCC(50.5, 32.24, 23)
     - YCC(12.34, 34.6. 10)
     - YCC(51.2, 30, 200.34)

    Invalid Examples:
     - YCC(-50.5, 0.24, 23)
     - YCC(234.34, -34.6. 10)
     - YCC(451.2, 30, 200.34)
    """

    @staticmethod
    def __checkIfValid(value):
        if any([True for i in value if type(i) not in [int, float]]): return False
        value = [int(i * 255) if type(i) == float else i for i in value]
        if len([i for i in value if i >= 0 and i <= 256]) != 3: return False
        
        return True
    


    def __init__(self, y: float, cb: float, cr: float, notPercent: bool = False):
        if self.__checkIfValid((y, cb, cr)):
            if not notPercent:
                if type(y) == float: y = int(y * 255)
                if type(cb) == float: cb = int(cb * 255)
                if type(cr) == float: cr = int(cr * 255)

            self.y = float(y)
            self.cb = float(cb)
            self.cr = float(cr)
            self.__valid = True
        
        else: self.__valid = False


    @property
    def rgb(self) -> tuple:
        if not self.__valid: return None

        r = int(round((self.y * 1.1643835616 + self.cr * 1.7927410714 - 248.100994), 3))
        g = int(round((self.y * 1.1643835616 + self.cb * -0.2132486143 + self.cr * -0.5329093286 + 76.878080), 3))
        b = int(round((self.y * 1.1643835616 + self.cb * 2.1124017857 - 289.017566), 3))

        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        
        return (r, g, b)
    

    @property
    def hexidecimal(self) -> tuple:
        if not self.__valid: return None

        r = hex(self.rgb[0])[2:].zfill(2).upper()
        g = hex(self.rgb[1])[2:].zfill(2).upper()
        b = hex(self.rgb[2])[2:].zfill(2).upper()

        return '#' + ''.join([r, g, b])
    

    @property
    def hsv(self) -> tuple:
        if not self.__valid: return None

        red = self.rgb[0]
        green = self.rgb[1]
        blue = self.rgb[2]

        M = max(red, green, blue)
        m = min(red, green, blue)

        V = (M / 255) * 100

        S = 0
        if M > 0: S = 100 - ((m / M) * 100)

        try:
            H = degrees(acos((red - (green / 2) - (blue / 2)) / sqrt((red ** 2) + (green ** 2) + (blue ** 2) - (red * green) - (red * blue) - (green * blue))))
            if blue > green: H = 360 - H
        except: H = 0
        if H != 0: H -= 1

        H = int(round(H))
        S = int(round(S))
        V = int(round(V))

        return (H, S, V)


    @property 
    def hsl(self) -> tuple:
        if not self.__valid: return None

        red = self.rgb[0]
        green = self.rgb[1]
        blue = self.rgb[2]

        M = max([red, green, blue])
        m = min([red, green, blue])

        M = max([(red / 255.0), (green / 255.0), (blue / 255.0)])
        m = min([(red / 255.0), (green / 255.0), (blue / 255.0)])

        C = M - m
        L = (M + m) / 2.0

        S = 0
        if C != 0: S = ((C / (1.0 - abs((2.0 * L) - 1.0))) * 100.0)
		
        try:
            H = degrees(acos((red - (green / 2) - (blue / 2)) / sqrt((red ** 2) + (green ** 2) + (blue ** 2) - (red * green) - (red * blue) - (green * blue))))
            if blue > green: H = 360 - H
        except: H = 0
        if H != 0: H -= 1

        H = int(round(H))
        S = int(round(S))
        L = int(round(L * 100.0))
			
        return (H, S, L)
    

    @property
    def xyz(self) -> tuple:
        if not self.__valid: return None

        r = self.rgb[0] / 255.0
        g = self.rgb[1] / 255.0
        b = self.rgb[2] / 255.0

        rgb = [(((i + 0.055) / 1.055) ** 2.4) if i > 0.04045 else (i / 12.92) for i in [r, g, b]]

        x = round((rgb[0] * 41.24 + rgb[1] * 35.76 + rgb[2] * 18.05), 2)
        y = round((rgb[0] * 21.26 + rgb[1] * 71.52 + rgb[2] * 7.22), 2)
        z = round((rgb[0] * 1.93 + rgb[1] * 11.92 + rgb[2] * 95.05), 2)

        return (x, y, z)
    

    @property
    def ycc(self) -> tuple:
        if not self.__valid: return None
        return (self.y, self.cb, self.cr)
    

    @property
    def cmyk(self) -> tuple:
        if not self.__valid: return None

        nr = self.rgb[0] / 255.0
        ng = self.rgb[1] / 255.0
        nb = self.rgb[2] / 255.0

        K = 1.0 - max(nr, ng, nb)

        C = int(round(((1 - nr - K) / (1 - K) * 100)))
        M = int(round(((1 - ng - K) / (1 - K) * 100)))
        Y = int(round(((1 - nb - K) / (1 - K) * 100)))
        K = int(round(K * 100))

        return (C, M, Y, K)

    
    @property
    def percentForm(self) -> tuple:
        if not self.__valid: return None

        y = round((self.cyan / 255.0), 2)
        cb = round((self.magenta / 255.0), 2)
        cr = round((self.yellow / 255.0), 2)

        return (y, cb, cr)
    

    @property
    def grayscale(self) -> tuple:
        if not self.__valid: return None

        gv = int(round((self.rgb[0] + self.rgb[1] + self.rgb[2]) / 3.0))
        rgbGray = RGB(gv, gv, gv)

        return YCC(*rgbGray.ycc)
    

    @property
    def greyscale(self) -> tuple: return self.grayscale
    

    def __repr__(self):
        if not self.__valid: return 'Invalid YCC'
        return str(self.y) + ' ' + str(self.cb) + ' ' + str(self.cr)
    



class CMYK:
    """
    CMYK color class object. 
    Takes in cyan, magenta, yellow, and key values.

    Attributes:
        cyan (int | float): An integer value between 0-100 or float value between 0-1.
        magenta (int | float): An integer value between 0-100 or float value between 0-1.
        yellow (int | float): An integer value between 0-100 or float value between 0-1.
        key (int | float): An integer value between 0-100 or float value between 0-1.

        
    Valid Examples:
     - CMYK(100, 100, 100, 100)
     - CMYK(100, 30, 80, 30)
     - CMYK(50, 30, 100, 0)

    Invalid Examples:
     - CMYK(2, 101, 50, 101)
     - CMYK(-3, 29, 290, 0)
     - CMYK(365, 123, 100, -100)
    """

    @staticmethod
    def __checkIfValid(value):
        if any([True for i in value if type(i) not in [int, float]]): return False
        value = [int(i * 100) if type(i) == float else i for i in value]
        return len([i for i in value if i >= 0 and i <= 100]) == 4



    def __init__(self, cyan: int | float, magenta: int | float, yellow: int | float, key: int | float, notPercent: bool = False):
        if self.__checkIfValid((cyan, magenta, yellow, key)):
            if not notPercent:
                if type(cyan) == float: cyan = int(cyan * 100)
                if type(magenta) == float: magenta = int(magenta * 100)
                if type(yellow) == float: yellow = int(yellow * 100)
                if type(key) == float: key = int(key * 100)

            self.cyan = cyan
            self.magenta = magenta
            self.yellow = yellow
            self.key = key
            self.__valid = True
        
        else: self.__valid = False
    

    @property
    def rgb(self) -> tuple:
        if not self.__valid: return None

        K = self.key / 100.0
        red = int(round(-255 * (((self.cyan / 100.0) * (1 - K)) - 1 + K)))
        green = int(round(-255 * (((self.magenta / 100.0) * (1 - K)) - 1 + K)))
        blue = int(round(-255 * (((self.yellow / 100.0) * (1 - K)) - 1 + K)))

        return (red, green, blue)


    @property
    def hexidecimal(self) -> str:
        if not self.__valid: return None

        r = hex(self.rgb[0])[2:].zfill(2).upper()
        g = hex(self.rgb[1])[2:].zfill(2).upper()
        b = hex(self.rgb[2])[2:].zfill(2).upper()

        return '#' + ''.join([r, g, b])
    

    @property
    def hsv(self) -> tuple:
        if not self.__valid: return None

        red = self.rgb[0]
        green = self.rgb[1]
        blue = self.rgb[2]

        M = max(red, green, blue)
        m = min(red, green, blue)

        V = (M / 255) * 100

        S = 0
        if M > 0: S = 100 - ((m / M) * 100)

        try:
            H = degrees(acos((red - (green / 2) - (blue / 2)) / sqrt((red ** 2) + (green ** 2) + (blue ** 2) - (red * green) - (red * blue) - (green * blue))))
            if blue > green: H = 360 - H
        except: H = 0
        if H != 0: H -= 1

        H = int(round(H))
        S = int(round(S))
        V = int(round(V))

        return (H, S, V)


    @property 
    def hsl(self) -> tuple:
        if not self.__valid: return None

        red = self.rgb[0]
        green = self.rgb[1]
        blue = self.rgb[2]

        M = max([red, green, blue])
        m = min([red, green, blue])

        M = max([(red / 255.0), (green / 255.0), (blue / 255.0)])
        m = min([(red / 255.0), (green / 255.0), (blue / 255.0)])

        C = M - m
        L = (M + m) / 2.0

        S = 0
        if C != 0: S = ((C / (1.0 - abs((2.0 * L) - 1.0))) * 100.0)
		
        try:
            H = degrees(acos((red - (green / 2) - (blue / 2)) / sqrt((red ** 2) + (green ** 2) + (blue ** 2) - (red * green) - (red * blue) - (green * blue))))
            if blue > green: H = 360 - H
        except: H = 0
        if H != 0: H -= 1

        H = int(round(H))
        S = int(round(S))
        L = int(round(L * 100.0))
			
        return (H, S, L)
    

    @property
    def xyz(self) -> tuple:
        if not self.__valid: return None

        r = self.rgb[0] / 255.0
        g = self.rgb[1] / 255.0
        b = self.rgb[2] / 255.0

        rgb = [(((i + 0.055) / 1.055) ** 2.4) if i > 0.04045 else (i / 12.92) for i in [r, g, b]]

        x = round((rgb[0] * 41.24 + rgb[1] * 35.76 + rgb[2] * 18.05), 2)
        y = round((rgb[0] * 21.26 + rgb[1] * 71.52 + rgb[2] * 7.22), 2)
        z = round((rgb[0] * 1.93 + rgb[1] * 11.92 + rgb[2] * 95.05), 2)

        return (x, y, z)
    

    @property
    def ycc(self) -> tuple:
        if not self.__valid: return None

        y = round((16 + ((65.738 * self.rgb[0]) / 256) + ((129.057 * self.rgb[1]) / 256) + ((25.064 * self.rgb[2]) / 256)), 2)
        cb = round((128 - ((37.945 * self.rgb[0]) / 256) - ((74.494 * self.rgb[1]) / 256) + ((112.439 * self.rgb[2]) / 256)), 2)
        cr = round((128 + ((112.439 * self.rgb[0]) / 256) - ((94.154 * self.rgb[1]) / 256) - ((18.285 * self.rgb[2]) / 256)), 2)

        return (y, cb, cr)
    

    @property
    def cmyk(self) -> tuple:
        if not self.__valid: return None
        return (self.cyan, self.magenta, self.yellow, self.key)
    

    @property
    def percentForm(self) -> tuple:
        if not self.__valid: return None

        c = round((self.cyan / 100.0), 2)
        m = round((self.magenta / 100.0), 2)
        y = round((self.yellow / 100.0), 2)
        k = round((self.key / 100.0), 2)

        return (c, m, y, k)
    

    @property
    def grayscale(self) -> tuple:
        if not self.__valid: return None

        gv = int(round((self.rgb[0] + self.rgb[1] + self.rgb[2]) / 3.0))
        rgbGray = RGB(gv, gv, gv)

        return CMYK(*rgbGray.cmyk)
    

    @property
    def greyscale(self) -> tuple: return self.grayscale


    
    def __repr__(self):
        if not self.__valid: return 'Invalid CMYK'
        return str(self.cyan) + '% ' + str(self.magenta) + '% ' + str(self.yellow) + '% ' + str(self.key) + '%'