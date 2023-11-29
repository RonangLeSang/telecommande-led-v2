import sys

from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication

from SSH.Connection import ConnectionAttempt
from Widgets.loadSetup import load_setup
from Widgets.setButtons import setup_window


def get_rgb():
    """
    Renvoie les valeurs rgb des curseurs
    :return:
    """
    return f"{window.valRed.value()}\n" \
           f"{window.valGreen.value()}\n" \
           f"{window.valBlue.value()}\n"


if __name__ == "__main__":

    # déclaration des variables

    ip_address = "192.168.1.53"
    username = "pi"
    password = "terrasnet"

    # fenêtre

    loader = QUiLoader()
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    window = loader.load("ressources\\UI\\fen.ui", None)

    connectionAttempt = ConnectionAttempt(ip_address, username, password, window)
    connectionAttempt.start()

    window.show()

    leds = load_setup(window)

    setup_window(window, leds)

    app.exec()

    # arrêt du programme

    connectionAttempt.isConnected = True
    connectionAttempt.join()
 