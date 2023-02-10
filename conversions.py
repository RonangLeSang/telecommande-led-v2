import json
from scipy.spatial import distance


def rgb_to_hex(r : int, g : int, b : int):
    """
    Renvoi un code hexadécimal à partir d'un code RGB sous le format # 00 00 00
    :param r: int
    :param g: int
    :param b: int
    :return: hexa
    """
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def hex_to_rgb(hex : hex):
    """
    À partir d'un code hexadecimal sous format # 00 00 00, retourne un tuple rgb
    :param hex: hexa
    :return (rgb): tuple RGB
    """
    hex = hex[1:]
    rgb = []
    for i in (0, 2, 4):
        decimal = int(hex[i:i + 2], 16)
        rgb.append(decimal)
    return tuple(rgb)


def closest_pantone(rgb):
    """
    Renvoi le code pantone le plus proche du tuple rgb en paramètre à l'aide d'un dictionnaire
    :param rgb: tuple
    :return rep: str code Pantone
    """
    with open("results.json", "r") as file:
        pantone = json.load(file)
        min_dist = 2555555
        pantoneKeys = pantone.keys()
        rep = min(pantoneKeys)
        for color_pantone in pantoneKeys:
            dist = distance.euclidean(tuple(pantone[color_pantone]), rgb)
            if dist < min_dist:
                min_dist = dist
                rep = color_pantone
    return rep


def pantone_to_rgb(code_pantone):
    """
    Retourne un tuple rgb à partir du code Pantone correspondant à l'aide d'un dictionnaire
    :param code_pantone: str
    :return (rgb): tuple rgb
    """
    with open("results.json", "r") as file:
        pantone = json.load(file)
    if code_pantone in pantone.keys():
        return pantone[code_pantone]
    else:
        return tuple([window.sliderRed.value(), window.sliderGreen.value(), window.sliderBlue.value()])

