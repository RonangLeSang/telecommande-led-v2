
def get_police_color(middleGrey: int):
    """
    Renvoi la couleur de police à utiliser en fonction du niveau de gris des boutons
    :param middleGrey: moyenne des couleurs
    :return: blanc ou noir
    """
    if middleGrey >= 128:
        return 0
    else:
        return 255


def get_middle_grey(window):
    """
    Retourne une valeur de gris en faisant la moyenne des paramètres R, G et B
    :return int:
    """
    return 255 - (window.sliderRed.value() + window.sliderGreen.value() + window.sliderBlue.value()) / 3
