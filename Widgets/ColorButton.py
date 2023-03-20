from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QApplication

from Memory.Pressed import get_is_pressed, switch_is_pressed
from Colors.conversions import rgb_to_hex


def press():
    switch_is_pressed()
    if get_is_pressed():
        QApplication.setOverrideCursor(Qt.CrossCursor)
    else:
        QApplication.setOverrideCursor(Qt.ArrowCursor)


class ColorButton(QFrame):

    def __init__(self, sliderR, sliderG, sliderB):
        super(ColorButton, self).__init__()
        self.sliderR = sliderR
        self.sliderG = sliderG
        self.sliderB = sliderB
        self.isPressed = False
        self.isLocked = False
        self.isHovered = False
        self.color = "#000000"
        self.setStyleSheet(f"background-color:white;\n"
                           f"border-radius: 1px;"
                           f"border: 1px solid black;")

    def color_your_button(self):
        self.isLocked = not self.isLocked
        if self.isLocked:
            self.setStyleSheet(f"background-color : rgb({self.sliderR.value()},{self.sliderG.value()},"
                               f"{self.sliderB.value()});\n"
                               f"border-radius: 3px;"
                               f"border: 3px solid blue;")
            self.color = rgb_to_hex(self.sliderR.value(), self.sliderG.value(), self.sliderB.value())
        else:
            self.setStyleSheet(f"background-color:white;\n"
                               f"border-radius: 1px;"
                               f"border: 1px solid black;")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and not self.isHovered:
            press()
            self.color_your_button()
        else:
            self.isHovered = False
            press()

    def enterEvent(self, event):
        if get_is_pressed():
            self.isHovered = True
            self.color_your_button()

    def leaveEvent(self, event):
        if get_is_pressed():
            self.isHovered = False
