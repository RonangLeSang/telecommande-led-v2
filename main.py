import sys
import os
import time
import paramiko

from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import QPropertyAnimation, QFile, QIODevice
from PySide6.QtWidgets import QFileDialog
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout
from PySide6.QtUiTools import QUiLoader
import threading


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


def set_button_color(middleGrey: int):
    policeColor = get_police_color(middleGrey)
    label_color(abs(policeColor - 255))

    window.colorLaunch.setStyleSheet(
        f"background-color: rgb({middleGrey},{middleGrey},{middleGrey});"
        f"padding: 15px;"
        f"color: rgb({policeColor},{policeColor},{policeColor});"
        f"border-radius: 20px;")

    window.launchHyperyon.setStyleSheet(
        f"background-color: rgb({middleGrey},{middleGrey},{middleGrey});"
        f"padding: 15px;"
        f"color: rgb({policeColor},{policeColor},{policeColor});"
        f"border-radius: 20px;")

    window.quitHyperyon.setStyleSheet(
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


def change_bg_spinbox():
    set_bg()
    window.sliderRed.setValue(window.valRed.value())
    window.sliderGreen.setValue(window.valGreen.value())
    window.sliderBlue.setValue(window.valBlue.value())


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
    affichage = ["En attente de connexion", "En attente de connexion.", "En attente de connexion..",
                 "En attente de connexion..."]
    window.connectionStatus.setText(affichage[i])


def launch_color():
    quit_hyperion()
    chaine = f"echo {window.valRed.value()}l>/home/pi/coucou.txt"
    stdin,stdout,stderr=ssh_client.exec_command(chaine)
    chaine = f"echo {window.valGreen.value()}l>>/home/pi/coucou.txt"
    stdin,stdout,stderr=ssh_client.exec_command(chaine)
    chaine = f"echo {window.valBlue.value()}l>>/home/pi/coucou.txt"
    stdin,stdout,stderr=ssh_client.exec_command(chaine)
    stdin,stdout,stderr=ssh_client.exec_command("python3 /home/pi/hue.py")


def launch_hyperion():
    stdin,stdout,stderr = ssh_client.exec_command("/usr/bin/hyperiond")


def quit_hyperion():
    stdin,stdout,stderr = ssh_client.exec_command("killall hyperiond")


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

    window.labelRed.setStyleSheet(
        f"color: rgb(255,255,255)")
    window.labelGreen.setStyleSheet(
        f"color: rgb(255,255,255)")
    window.labelBlue.setStyleSheet(
        f"color: rgb(255,255,255)")

    window.colorLaunch.clicked.connect(launch_color)
    window.launchHyperyon.clicked.connect(launch_hyperion)
    window.quitHyperyon.clicked.connect(quit_hyperion)

    app.exec()

    # arrêt du programme

    connectionAttempt.isConnected = True
    connectionAttempt.join()
