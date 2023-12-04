import sys

from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication

from Memory.Pressed import set_connection_attempt
from SSH.Connection import ConnectionAttempt
from SSH.ID import get_id_from_file
from Widgets.loadSetup import load_setup, get_last_setup
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

    # fenêtre

    loader = QUiLoader()
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    window = loader.load("ressources\\UI\\fen.ui", None)

    connectionAttempt = ConnectionAttempt(get_id_from_file(get_last_setup()), window)
    connectionAttempt.start()
    set_connection_attempt(connectionAttempt)

    window.show()

    leds = load_setup(window)

    setup_window(window, leds)

    app.exec()

    # arrêt du programme

    connectionAttempt.isConnected = True
    connectionAttempt.join()
 