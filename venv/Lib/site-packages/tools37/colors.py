HEX = "0123456789ABCDEF"

BLACK = '#000000'
WHITE = '#FFFFFF'
RED = '#FF0000'
GREEN = '#00FF00'
BLUE = '#0000FF'
CYAN = '#00FFFF'
PURPLE = '#FF00FF'
YELLOW = '#FFFF00'
GRAY = '#777777'


def is_hex_code(hex: str):
    """return True if the given string is a valid hexadecimal color code"""
    # TODO : add minified hexadecimal codes such as "#FF0"
    return len(hex) == 7 and hex[0] == '#' and all(char in HEX for char in hex[1:].upper())


def hex_to_rgb(hex: str) -> (int, int, int):
    """this function turns hexadecimal color codes into rgb tuple"""
    # TODO : add minified hexadecimal codes such as "#FF0"
    hex = hex.upper()
    if not is_hex_code(hex):
        raise ValueError(hex)

    r = 16 * HEX.index(hex[1]) + HEX.index(hex[2])
    g = 16 * HEX.index(hex[3]) + HEX.index(hex[4])
    b = 16 * HEX.index(hex[5]) + HEX.index(hex[6])

    return r, g, b


def rgb_to_hex(rgb: (int, int, int)) -> str:
    """this function turns rgb tuple into hexadecimal color codes"""
    # TODO : add minified hexadecimal codes such as "#FF0"
    if not all(0 <= c < 256 for c in rgb):
        raise ValueError(rgb)

    r1, r2 = divmod(rgb[0], 16)
    g1, g2 = divmod(rgb[1], 16)
    b1, b2 = divmod(rgb[2], 16)

    return '#' + HEX[r1] + HEX[r2] + HEX[g1] + HEX[g2] + HEX[b1] + HEX[b2]
