import sys
import os
import time
import paramiko
import threading
import json

from functools import partial
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import QPropertyAnimation, QFile, QIODevice
from PySide6.QtWidgets import QFileDialog, QLabel, QWidget
from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout
from PySide6.QtUiTools import QUiLoader
from scipy.spatial import distance


class ConnectionAttempt(threading.Thread):
    def __init__(self, ip_address, username, password):
        threading.Thread.__init__(self)
        self.isConnected = False
        self.ip_address = ip_address
        self.username = username
        self.password = password

    def run(self):
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
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop = False

    def run(self):
        time.sleep(2)
        i = 0
        while not self.stop:
            wait_connection(i)
            time.sleep(0.2)
            if i == 3:
                i = 0
            else:
                i += 1


class LedButton:
    def __init__(self, button):
        self.button = button
        self.isLocked = False
        self.color = "#000000"


def rgb_to_hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def hex_to_rgb(hex):
    hex = hex[1:]
    rgb = []
    for i in (0, 2, 4):
        decimal = int(hex[i:i + 2], 16)
        rgb.append(decimal)
    return tuple(rgb)


def closest_pantone(rgb):
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
    with open("results.json", "r") as file:
        pantone = json.load(file)
    if code_pantone in pantone.keys():
        return pantone[code_pantone]
    else:
        return tuple([window.sliderRed.value(), window.sliderGreen.value(), window.sliderBlue.value()])


def get_middle_grey():
    return 255 - (window.sliderRed.value() + window.sliderGreen.value() + window.sliderBlue.value()) / 3


def get_police_color(middleGrey: int):
    if middleGrey >= 128:
        return 0
    else:
        return 255


def label_color(color: int):
    window.labelRed.setStyleSheet(
        f"color: rgb({color},{color},{color})")
    window.labelGreen.setStyleSheet(
        f"color: rgb({color},{color},{color})")
    window.labelBlue.setStyleSheet(
        f"color: rgb({color},{color},{color})")
    window.connectionStatus.setStyleSheet(
        f"color: rgb({color},{color},{color})")
    window.labelHexa.setStyleSheet(
        f"color: rgb({color},{color},{color})")
    window.labelPantone.setStyleSheet(
        f"color: rgb({color},{color},{color})")
    window.editHexa.setStyleSheet(
        f"color: rgb({color},{color},{color});\n"
        f"border: 0px;")
    window.editPantone.setStyleSheet(
        f"color: rgb({color},{color},{color});\n"
        f"border: 0px;")


def set_button_color(middleGrey: int):
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


def set_bg():
    window.setStyleSheet(
        f"background-color : rgb({window.sliderRed.value()},{window.sliderGreen.value()},{window.sliderBlue.value()})")
    set_button_color(get_middle_grey())


def change_bg_sliders():
    set_bg()
    window.valRed.setValue(window.sliderRed.value())
    window.valGreen.setValue(window.sliderGreen.value())
    window.valBlue.setValue(window.sliderBlue.value())
    window.editHexa.setText(rgb_to_hex(window.sliderRed.value(), window.sliderGreen.value(), window.sliderBlue.value()))
    window.editPantone.setText(
        closest_pantone((window.sliderRed.value(), window.sliderGreen.value(), window.sliderBlue.value())))


def change_bg_spinbox():
    set_bg()
    window.sliderRed.setValue(window.valRed.value())
    window.sliderGreen.setValue(window.valGreen.value())
    window.sliderBlue.setValue(window.valBlue.value())


def change_bg_hex():
    if len(window.editHexa.text()) == 7:
        hex = hex_to_rgb(window.editHexa.text())
        window.sliderRed.setValue(hex[0])
        window.sliderGreen.setValue(hex[1])
        window.sliderBlue.setValue(hex[2])


def change_bg_pantone():
    rgb = pantone_to_rgb(window.editPantone.text())
    window.sliderRed.setValue(rgb[0])
    window.sliderGreen.setValue(rgb[1])
    window.sliderBlue.setValue(rgb[2])


def get_rgb():
    return f"{window.valRed.value()}\n" \
           f"{window.valGreen.value()}\n" \
           f"{window.valBlue.value()}\n"


def connect(ip_address, username, password, connectionWait):
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


def not_connected():
    window.connectionStatus.setText("échec de la connection")


def connected():
    window.connectionStatus.setText(f"connecté à : {ip_address}")


def wait_connection(i):
    affichage = ["En attente de connexion   ", "En attente de connexion.  ", "En attente de connexion.. ",
                 "En attente de connexion..."]
    window.connectionStatus.setText(affichage[i])


def launch_color():
    quit_hyperion()
    chaine = f"echo {window.valRed.value()}l>/home/pi/coucou.txt"
    stdin, stdout, stderr = ssh_client.exec_command(chaine)
    chaine = f"echo {window.valGreen.value()}l>>/home/pi/coucou.txt"
    stdin, stdout, stderr = ssh_client.exec_command(chaine)
    chaine = f"echo {window.valBlue.value()}l>>/home/pi/coucou.txt"
    stdin, stdout, stderr = ssh_client.exec_command(chaine)
    stdin, stdout, stderr = ssh_client.exec_command("python3 /home/pi/hue.py")


def launch_hyperion():
    stdin, stdout, stderr = ssh_client.exec_command("/usr/bin/hyperiond")


def quit_hyperion():
    stdin, stdout, stderr = ssh_client.exec_command("killall hyperiond")


def led_clicked(indice, leds):
    if not leds[indice].isLocked:
        leds[indice].button.setStyleSheet(f"border-radius: 3px;"
                                    f"border: 2px solid blue;"
                                    f"outline: solid;"
                                    f"background-color: rgb({window.sliderRed.value()},{window.sliderGreen.value()},{window.sliderBlue.value()});")
    else:
        leds[indice].button.setStyleSheet(f"background-color : white;"
                                          f"border-radius: 3px;")
    leds[indice].isLocked = not leds[indice].isLocked


if __name__ == "__main__":

    # déclaration des variables

    global ip_address
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

    ledsButton = [window.ledButton1, window.ledButton2, window.ledButton3, window.ledButton4, window.ledButton5,
            window.ledButton6, window.ledButton7, window.ledButton8, window.ledButton9, window.ledButton10,
            window.ledButton11, window.ledButton12, window.ledButton13, window.ledButton14, window.ledButton15,
            window.ledButton16, window.ledButton17, window.ledButton18, window.ledButton19, window.ledButton20,
            window.ledButton21, window.ledButton22, window.ledButton23, window.ledButton24, window.ledButton25,
            window.ledButton26, window.ledButton27, window.ledButton28, window.ledButton29, window.ledButton30,
            window.ledButton31, window.ledButton32, window.ledButton33, window.ledButton34, window.ledButton35,
            window.ledButton36, window.ledButton37, window.ledButton38, window.ledButton39, window.ledButton40,
            window.ledButton41, window.ledButton42, window.ledButton43, window.ledButton44, window.ledButton45,
            window.ledButton46, window.ledButton47, window.ledButton48, window.ledButton49, window.ledButton50,
            window.ledButton51, window.ledButton52, window.ledButton53, window.ledButton54, window.ledButton55,
            window.ledButton56, window.ledButton57, window.ledButton58, window.ledButton59, window.ledButton60,
            window.ledButton61, window.ledButton62, window.ledButton63, window.ledButton64, window.ledButton65,
            window.ledButton66, window.ledButton67, window.ledButton68, window.ledButton69, window.ledButton70,
            window.ledButton71, window.ledButton72, window.ledButton73, window.ledButton74, window.ledButton75,
            window.ledButton76, window.ledButton77, window.ledButton78, window.ledButton79, window.ledButton80,
            window.ledButton81, window.ledButton82, window.ledButton83, window.ledButton84, window.ledButton85,
            window.ledButton86, window.ledButton87, window.ledButton88, window.ledButton89, window.ledButton90,
            window.ledButton91, window.ledButton92, window.ledButton93, window.ledButton94, window.ledButton95,
            window.ledButton96, window.ledButton97, window.ledButton98, window.ledButton99, window.ledButton100,
            window.ledButton101, window.ledButton102, window.ledButton103, window.ledButton104, window.ledButton105,
            window.ledButton106, window.ledButton107, window.ledButton108]

    leds = []
    for led in ledsButton:
        leds.append(LedButton(led))

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

    for i in range(len(leds)):
        leds[i].button.clicked.connect(partial(led_clicked, i, leds))

    app.exec()

    # arrêt du programme

    connectionAttempt.isConnected = True
    connectionAttempt.join()
