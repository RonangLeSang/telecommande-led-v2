import json
import threading

from scipy.spatial import distance


class ClosestPantone(threading.Thread):

    def __init__(self, rgb, window):
        threading.Thread.__init__(self)
        self.rgb = rgb
        self.window = window

    def run(self):
        """
        Renvoi le code pantone le plus proche du tuple rgb en paramètre à l'aide d'un dictionnaire
        :param rgb: tuple
        :return rep: str code Pantone
        """
        with open("ressources/colors/results.json", "r") as file:
            pantone = json.load(file)
            min_dist = 2555555
            pantoneKeys = pantone.keys()
            rep = min(pantoneKeys)
            for color_pantone in pantoneKeys:
                dist = distance.euclidean(tuple(pantone[color_pantone]), self.rgb)
                if dist < min_dist:
                    min_dist = dist
                    rep = color_pantone
        self.window.editPantone.setText(rep)
