
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


