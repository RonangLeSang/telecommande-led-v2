import json

from PySide6.QtWidgets import QFileDialog

from Memory.Pressed import get_current_frame, get_saved_frames, set_saved_frames, set_current_frame
from Colors.conversions import rgb_to_hex, hex_to_rgb


def indicate_page(window, savedFrames, currentFrame):
    window.pageIndicator.setText(f"frame : {currentFrame+1}/{len(savedFrames)+1}")
    set_saved_frames(savedFrames)
    set_current_frame(currentFrame)


def clean_boxes(leds):
    for i in range(0, len(leds)):
        if leds[i].isLocked:
            leds[i].color_your_button()


def back_frame(leds, window):
    """
    Affiche la frame d'animation précédente
    """
    currentFrame = get_current_frame()
    savedFrames = get_saved_frames()
    change_frame(currentFrame, savedFrames, leds, window)
    if currentFrame > 0:
        load_frame(savedFrames[currentFrame - 1], leds, window)
        display_frame(leds)
        currentFrame -= 1
        indicate_page(window, savedFrames, currentFrame)


def next_frame(leds, window):
    """
    Affiche la frame d'animation suivante
    """
    currentFrame = get_current_frame()
    savedFrames = get_saved_frames()
    change_frame(currentFrame, savedFrames, leds, window)
    if currentFrame == len(savedFrames)-1:
        clean_boxes(leds)
    else:
        load_frame(savedFrames[currentFrame + 1], leds, window)
        display_frame(leds)
    currentFrame += 1
    indicate_page(window, savedFrames, currentFrame)


def change_frame(currentFrame, savedFrames, leds, window):
    """
    Gère la sauvegarde et la modification de frames en fonction de l'indice et de la longueur de la liste
    :param leds:
    :param window:
    :param currentFrame:
    :param savedFrames:
    :return:
    """
    if currentFrame == len(savedFrames):
        save_frame(leds, savedFrames, window)
    else:
        modif_frame(leds, savedFrames, currentFrame, window)


def save(saveButton):
    """
    Sauvegarde un fichier d'animation
    """
    try:
        fileName = QFileDialog.getSaveFileName(saveButton, "Save animation", "ressources/saves", "Json Files (*.json)")
        with open(fileName[0], "w") as file:
            file.write(json.dumps(get_saved_frames()))
    except FileNotFoundError:
        pass


def save_frame(leds, save, window):
    """
    Sauvegarde une frame d'animation
    """
    frame = [window.timeChoose.value()]
    for led in leds:
        if not led.isLocked:
            led.color = rgb_to_hex(window.sliderRed.value(), window.sliderGreen.value(), window.sliderBlue.value())
        frame.append(led.color)
    save.append(frame)


def modif_frame(leds, savedFrames, indice, window):
    """
    modifie une frame
    :param leds:
    :param indice:
    """
    frame = [window.timeChoose.value()]
    for led in leds:
        if not led.isLocked:
            led.color = rgb_to_hex(window.sliderRed.value(), window.sliderGreen.value(), window.sliderBlue.value())
        frame.append(led.color)
    savedFrames[indice] = frame


def display_frame(leds):
    for led in leds:
        ledColor = hex_to_rgb(led.color)
        led.setStyleSheet(f"border-radius: 3px;"
                                 f"border: 2px solid blue;"
                                 f"outline: solid;"
                                 f"background-color: rgb({ledColor[0]},{ledColor[1]}, {ledColor[2]});")


def load_frame(frame, leds, window):
    window.timeChoose.setValue(frame[0])
    for i in range(1, len(leds)):
        leds[i].color = frame[i]
        leds[i].isLocked = True


def load(window, loadButton, leds):
    """
    Charge un fichier d'animation
    """
    try:
        fileName = QFileDialog.getOpenFileName(loadButton, "Load animation", "ressources/saves", "Json Files (*.json)")
        with open(fileName[0], "r") as file:
            set_saved_frames(json.load(file))
        set_current_frame(len(get_saved_frames())-1)
        next_frame(leds, window)
    except FileNotFoundError:
        pass


def suppress_frame(window, leds):
    savedFrames = get_saved_frames()
    currentFrame = get_current_frame()
    savedFrames.pop(get_current_frame())
    set_saved_frames(savedFrames)
    if currentFrame > 0:
        load_frame(savedFrames[currentFrame - 1], leds, window)
        display_frame(leds)
        currentFrame -= 1
        indicate_page(window, savedFrames, currentFrame)
