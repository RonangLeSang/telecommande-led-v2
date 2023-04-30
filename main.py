import sys

from functools import partial
from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader

from Widgets.Animations import back_frame, next_frame, save, load, suppress_frame, insert_animation
from Widgets.ColorWidget import change_bg_hex, change_bg_pantone, change_bg_sliders
from SSH.Connection import ConnectionAttempt
from SSH.SSHCommands import launch_color, launch_hyperion, quit_hyperion
from Widgets.loadSetup import load_setup


def get_rgb():
    """
    Renvoie les valeurs rgb des curseurs
    :return:
    """
    return f"{window.valRed.value()}\n" \
           f"{window.valGreen.value()}\n" \
           f"{window.valBlue.value()}\n"


def setup_window(leds):
    window.setStyleSheet(f"background-color : black")
    # window.menuCouleur.setStyleSheet(f"background-color : white")

    window.sliderRed.setMaximum(255)
    window.sliderGreen.setMaximum(255)
    window.sliderBlue.setMaximum(255)

    changeBack = partial(change_bg_sliders, window)

    window.sliderRed.valueChanged.connect(changeBack)
    window.sliderGreen.valueChanged.connect(changeBack)
    window.sliderBlue.valueChanged.connect(changeBack)

    window.timeChoose.setMaximum(3600000)
    window.valRed.setMaximum(255)
    window.valGreen.setMaximum(255)
    window.valBlue.setMaximum(255)

    changeSpin = partial(change_bg_sliders, window)

    window.valRed.valueChanged.connect(changeSpin)
    window.valGreen.valueChanged.connect(changeSpin)
    window.valBlue.valueChanged.connect(changeSpin)
    window.editHexa.textChanged.connect(partial(change_bg_hex, window))
    window.editPantone.returnPressed.connect(partial(change_bg_pantone, window))

    window.colorLaunch.clicked.connect(partial(launch_color, window))
    window.launchHyperyon.clicked.connect(launch_hyperion)
    window.quitHyperyon.clicked.connect(quit_hyperion)

    window.backButton.clicked.connect(partial(back_frame, leds, window))
    window.nextButton.clicked.connect(partial(next_frame, leds, window))
    window.saveButton.clicked.connect(partial(save, window.saveButton))
    window.loadButton.clicked.connect(partial(load, window, window.loadButton, leds))

    window.suppressFrame.triggered.connect(partial(suppress_frame, window, leds))
    window.insertAnimation.triggered.connect(partial(insert_animation, window, leds))


if __name__ == "__main__":

    # déclaration des variables

    ip_address = "192.168.1.53"
    username = "pi"
    password = "terrasnet"

    # fenêtre

    loader = QUiLoader()
    app = QtWidgets.QApplication(sys.argv)
    window = loader.load("ressources\\UI\\fen.ui", None)

    connectionAttempt = ConnectionAttempt(ip_address, username, password, window)
    connectionAttempt.start()

    window.show()

    leds = load_setup(window.sliderRed, window.sliderGreen, window.sliderBlue, window)

    setup_window(leds)

    app.exec()

    # arrêt du programme

    connectionAttempt.isConnected = True
    connectionAttempt.join()
