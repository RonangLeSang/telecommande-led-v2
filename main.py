import sys
import time
import paramiko
import threading
import json

from functools import partial
from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader

from colors import get_police_color
from conversions import rgb_to_hex, hex_to_rgb, closest_pantone
from loadSetup import load_setup


# connection

class ConnectionAttempt(threading.Thread):
    """
    Thread qui tente de se connecter au raspberry
    """

    def __init__(self, ip_address, username, password):
        threading.Thread.__init__(self)
        self.isConnected = False
        self.ip_address = ip_address
        self.username = username
        self.password = password

    def run(self):
        """
        Continue d'essayer de se connecter tant qu'il n'y arrive pas et marque de courtes pauses
        """
        while not self.isConnected:
            connectionWait = ConnectionWait()
            connectionWait.start()
            if not connect(ip_address, username, password, connectionWait):
                time.sleep(5)
            else:
                self.isConnected = True
            connectionWait.stop = True
            connectionWait.join()


class ConnectionWait(threading.Thread):
    """
    affiche un visuel d'attente de connection
    """

    def __init__(self):
        threading.Thread.__init__(self)
        self.stop = False

    def run(self):
        """
        Affiche un visuel jusqu'à la connection
        """
        time.sleep(2)
        i = 0
        while not self.stop:
            wait_connection(i)
            time.sleep(0.2)
            if i == 3:
                i = 0
            else:
                i += 1


def connect(ip_address, username, password, connectionWait):
    """
    Tente une connection en SSH en renvoie l'état de connection
    :param ip_address:
    :param username:
    :param password:
    :param connectionWait:
    :return: l'état de connection
    """
    global ssh_client
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(hostname=ip_address, username=username, password=password)
        remote_connection = ssh_client.invoke_shell()
        connectionWait.stop = True
        connectionWait.join()
        connected()
        return True
    except:
        connectionWait.stop = True
        connectionWait.join()
        not_connected()
        return False


# couleurs

def get_middle_grey():
    """
    Retourne une valeur de gris en faisant la moyenne des paramètres R, G et B
    :return int:
    """
    return 255 - (window.sliderRed.value() + window.sliderGreen.value() + window.sliderBlue.value()) / 3


def label_color(color: int):
    """
    Change la couleur des labels en fonction du fond
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


def set_button_color(middleGrey: int):
    """
    Change la couleur des bouttons en fonction du fond
    :param middleGrey: niveau de gris
    """
    policeColor = get_police_color(middleGrey)
    label_color(abs(policeColor - 255))

    buttons = [window.colorLaunch, window.launchHyperyon, window.quitHyperyon, window.backButton, window.nextButton,
               window.saveButton, window.loadButton]

    for button in buttons:
        button.setStyleSheet(
            f"background-color: rgb({middleGrey},{middleGrey},{middleGrey});"
            f"padding: 15px;"
            f"color: rgb({policeColor},{policeColor},{policeColor});"
            f"border-radius: 20px;")


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


def set_bg():
    """
    Change la couleur de fond en fonction des valeurs de curseurs
    """
    window.setStyleSheet(
        f"background-color : rgb({window.sliderRed.value()},{window.sliderGreen.value()},{window.sliderBlue.value()})")
    set_button_color(get_middle_grey())


def change_bg_sliders():
    """
    Change la couleur de fond et des labels en fonction des valeurs de curseurs
    """
    set_bg()
    window.valRed.setValue(window.sliderRed.value())
    window.valGreen.setValue(window.sliderGreen.value())
    window.valBlue.setValue(window.sliderBlue.value())
    window.editHexa.setText(rgb_to_hex(window.sliderRed.value(), window.sliderGreen.value(), window.sliderBlue.value()))
    window.editPantone.setText(
        closest_pantone((window.sliderRed.value(), window.sliderGreen.value(), window.sliderBlue.value())))


def change_bg_spinbox():
    """
    Change la couleur de fond et des labels en fonction des valeurs de spinbox
    """
    set_bg()
    window.sliderRed.setValue(window.valRed.value())
    window.sliderGreen.setValue(window.valGreen.value())
    window.sliderBlue.setValue(window.valBlue.value())


def change_bg_hex():
    """
    Change la couleur de fond et des labels en fonction de la valeur hexadécimale rentrée par l'utilisateur
    """
    if len(window.editHexa.text()) == 7:
        hex = hex_to_rgb(window.editHexa.text())
        window.sliderRed.setValue(hex[0])
        window.sliderGreen.setValue(hex[1])
        window.sliderBlue.setValue(hex[2])


def change_bg_pantone():
    """
    Change la couleur de fond et des labels en fonction du code pantone rentrée par l'utilisateur
    """
    rgb = pantone_to_rgb(window.editPantone.text())
    window.sliderRed.setValue(rgb[0])
    window.sliderGreen.setValue(rgb[1])
    window.sliderBlue.setValue(rgb[2])


def get_rgb():
    """
    Renvoie les valeurs rgb des curseurs
    :return:
    """
    return f"{window.valRed.value()}\n" \
           f"{window.valGreen.value()}\n" \
           f"{window.valBlue.value()}\n"


# affichage

def not_connected():
    """
    Affiche l'échec de connection sur l'écran
    """
    window.connectionStatus.setText("échec de la connection")


def connected():
    """
    Affiche la réussite de connection sur l'écran
    """
    window.connectionStatus.setText(f"connecté à : {ip_address}")


def wait_connection(i):
    """
    Affiche l'attente de connection en fonction de l'indice
    """
    affichage = ["En attente de connexion   ", "En attente de connexion.  ", "En attente de connexion.. ",
                 "En attente de connexion..."]
    window.connectionStatus.setText(affichage[i])


def indicate_page():
    global currentFrame
    global savedFrames
    window.pageIndicator.setText(f"frame : {currentFrame+1}/{len(savedFrames)+1}")


# commandes SSH

def launch_color():
    """
    Quitte Hyperion et envoi la couleur choisi dans un fichier par SSH
    """
    quit_hyperion()
    chaine = f"echo {window.valRed.value()}l>/home/pi/coucou.txt"
    stdin, stdout, stderr = ssh_client.exec_command(chaine)
    chaine = f"echo {window.valGreen.value()}l>>/home/pi/coucou.txt"
    stdin, stdout, stderr = ssh_client.exec_command(chaine)
    chaine = f"echo {window.valBlue.value()}l>>/home/pi/coucou.txt"
    stdin, stdout, stderr = ssh_client.exec_command(chaine)
    stdin, stdout, stderr = ssh_client.exec_command("python3 /home/pi/hue.py")


def launch_hyperion():
    """
    Lance Hyperion par SSH
    """
    stdin, stdout, stderr = ssh_client.exec_command("/usr/bin/hyperiond")


def quit_hyperion():
    """
    Quitte Hyperion par SSH
    """
    stdin, stdout, stderr = ssh_client.exec_command("killall hyperiond")


# animations

def clean_boxes(leds):
    for i in range(0, len(leds)):
        if leds[i].isLocked:
            led_clicked(i, leds)


def back_frame(leds):
    """
    Affiche la frame d'animation précédente
    """
    global currentFrame
    global savedFrames
    change_frame(currentFrame, savedFrames)
    if currentFrame > 0:
        load_frame(savedFrames[currentFrame - 1], leds)
        display_frame(leds)
        currentFrame -= 1
        indicate_page()


def next_frame():
    """
    Affiche la frame d'animation suivante
    """
    global currentFrame
    global savedFrames
    change_frame(currentFrame, savedFrames)
    if currentFrame == len(savedFrames)-1:
        clean_boxes(leds)
    else:
        load_frame(savedFrames[currentFrame + 1], leds)
        display_frame(leds)
    currentFrame += 1
    indicate_page()


def change_frame(currentFrame, savedFrames):
    """
    Gère la sauvegarde et la modification de frames en fonction de l'indice et de la longueur de la liste
    :param currentFrame:
    :param savedFrames:
    :return:
    """
    if currentFrame == len(savedFrames):
        save_frame(leds, savedFrames)
    else:
        modif_frame(leds, savedFrames, currentFrame)


def save():
    """
    Sauvegarde un fichier d'animation
    """
    pass


def save_frame(leds, save):
    """
    Sauvegarde une frame d'animation
    """
    frame = []
    for led in leds:
        if not led.isLocked:
            led.color = rgb_to_hex(window.sliderRed.value(), window.sliderGreen.value(), window.sliderBlue.value())
        frame.append(led.color)
    save.append(frame)


def modif_frame(leds, savedFrames, indice):
    """
    modifie une frame
    :param leds:
    :param save:
    :param indice:
    :return:
    """
    frame = []
    for led in leds:
        if not led.isLocked:
            led.color = rgb_to_hex(window.sliderRed.value(), window.sliderGreen.value(), window.sliderBlue.value())
        frame.append(led.color)
    savedFrames[indice] = frame


def display_frame(leds):
    for led in leds:
        ledColor = hex_to_rgb(led.color)
        led.button.setStyleSheet(f"border-radius: 3px;"
                                 f"border: 2px solid blue;"
                                 f"outline: solid;"
                                 f"background-color: rgb({ledColor[0]},{ledColor[1]}, {ledColor[2]});")


def load_frame(frame, leds):
    for i in range(0, len(leds)):
        leds[i].color = frame[i]
        leds[i].isLocked = True


def load():
    """
    Charge un fichier d'animation
    """
    pass


if __name__ == "__main__":

    # déclaration des variables

    global savedFrames
    global currentFrame
    global ip_address
    global isPressed
    isPressed = False
    currentFrame = 0
    savedFrames = []

    ip_address = "192.168.1.53"
    username = "pi"
    password = "terrasnet"

    # démarrage des threads

    connectionAttempt = ConnectionAttempt(ip_address, username, password)
    connectionAttempt.start()

    # fenêtre

    loader = QUiLoader()
    app = QtWidgets.QApplication(sys.argv)
    window = loader.load("fen.ui", None)
    window.show()

    window.setStyleSheet(
        f"background-color : rgb({0},{0},{0})")

    leds = load_setup(f"ressources\\setup\\telero.txt", window.sliderRed, window.sliderGreen, window.sliderBlue, window)

    window.sliderRed.setMaximum(255)
    window.sliderGreen.setMaximum(255)
    window.sliderBlue.setMaximum(255)

    window.sliderRed.valueChanged.connect(change_bg_sliders)
    window.sliderGreen.valueChanged.connect(change_bg_sliders)
    window.sliderBlue.valueChanged.connect(change_bg_sliders)

    window.valRed.setMaximum(255)
    window.valGreen.setMaximum(255)
    window.valBlue.setMaximum(255)

    window.valRed.valueChanged.connect(change_bg_spinbox)
    window.valGreen.valueChanged.connect(change_bg_spinbox)
    window.valBlue.valueChanged.connect(change_bg_spinbox)
    window.editHexa.textChanged.connect(change_bg_hex)
    window.editPantone.returnPressed.connect(change_bg_pantone)

    window.colorLaunch.clicked.connect(launch_color)
    window.launchHyperyon.clicked.connect(launch_hyperion)
    window.quitHyperyon.clicked.connect(quit_hyperion)

    window.backButton.clicked.connect(partial(back_frame, leds))
    window.nextButton.clicked.connect(next_frame)
    window.saveButton.clicked.connect(save)
    window.loadButton.clicked.connect(load)

    app.exec()

    # arrêt du programme

    connectionAttempt.isConnected = True
    connectionAttempt.join()
