from Colors.Closest_pantone import ClosestPantone
from Colors.conversions import hex_to_rgb, pantone_to_rgb, rgb_to_hex
from Colors.SetColor import set_bg


def change_bg_sliders(window, yo):
    """
    Change la couleur de fond et des labels en fonction des valeurs de curseurs
    """
    set_bg(window)
    window.valRed.setValue(window.sliderRed.value())
    window.valGreen.setValue(window.sliderGreen.value())
    window.valBlue.setValue(window.sliderBlue.value())
    window.editHexa.setText(rgb_to_hex(window.sliderRed.value(), window.sliderGreen.value(), window.sliderBlue.value()))
    closestPantone = ClosestPantone((window.sliderRed.value(), window.sliderGreen.value(), window.sliderBlue.value()),
                                    window)
    closestPantone.start()


def change_bg_spinbox(window, yo):
    """
    Change la couleur de fond et des labels en fonction des valeurs de spinbox
    """
    set_bg(window)
    window.sliderRed.setValue(window.valRed.value())
    window.sliderGreen.setValue(window.valGreen.value())
    window.sliderBlue.setValue(window.valBlue.value())


def change_bg_hex(window, yo):
    """
    Change la couleur de fond et des labels en fonction de la valeur hexadécimale rentrée par l'utilisateur
    """
    if len(window.editHexa.text()) == 7:
        hex = hex_to_rgb(window.editHexa.text())
        window.sliderRed.setValue(hex[0])
        window.sliderGreen.setValue(hex[1])
        window.sliderBlue.setValue(hex[2])


def change_bg_pantone(window):
    """
    Change la couleur de fond et des labels en fonction du code pantone rentrée par l'utilisateur
    """
    rgb = pantone_to_rgb(window.editPantone.text(), window)
    window.sliderRed.setValue(rgb[0])
    window.sliderGreen.setValue(rgb[1])
    window.sliderBlue.setValue(rgb[2])
