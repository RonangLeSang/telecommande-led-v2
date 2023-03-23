from Colors.colors import get_police_color, get_middle_grey


def label_color(color, window):
    """
    Change la couleur des labels en fonction du fond
    :param window:
    :param color: niveau de gris
    """
    labels = [window.labelRed, window.labelGreen, window.labelBlue, window.connectionStatus, window.labelHexa,
              window.labelPantone, window.tpsLabel, window.msLabel]
    spinBoxes = [window.editHexa, window.editPantone, window.pageIndicator]

    for label in labels:
        label.setStyleSheet(
            f"color: rgb({color},{color},{color})")
    for spinBoxe in spinBoxes:
        spinBoxe.setStyleSheet(
            f"color: rgb({color},{color},{color});\n"
            f"border: 0px;")


def set_button_color(middleGrey, window):
    """
    Change la couleur des bouttons en fonction du fond
    :param window:
    :param middleGrey: niveau de gris
    """
    policeColor = get_police_color(middleGrey)
    label_color(abs(policeColor - 255), window)

    buttons = [window.colorLaunch, window.launchHyperyon, window.quitHyperyon, window.backButton, window.nextButton,
               window.saveButton, window.loadButton, window.menuCouleur]

    for button in buttons:
        button.setStyleSheet(
            f"background-color: rgb({middleGrey},{middleGrey},{middleGrey});"
            f"padding: 15px;"
            f"color: rgb({policeColor},{policeColor},{policeColor});"
            f"border-radius: 20px;")


def set_bg(window):
    """
    Change la couleur de fond en fonction des valeurs de curseurs
    """
    window.setStyleSheet(
        f"background-color : rgb({window.sliderRed.value()},{window.sliderGreen.value()},{window.sliderBlue.value()})")
    set_button_color(get_middle_grey(window), window)
