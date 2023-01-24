import sys
import os
import time
from functools import partial

from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import QPropertyAnimation, QFile, QIODevice
from PySide6.QtWidgets import QFileDialog
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout
from PySide6.QtUiTools import QUiLoader


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


def get_ip():
    pass


def not_connected():
    window.connectionStatus.setText("en attente de connection ...")


def connected():
    pass


def launch_color():
    pass


def launch_hyperion():
    pass


def quit_hyperion():
    pass


if __name__ == "__main__":
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

    not_connected()

    app.exec()
