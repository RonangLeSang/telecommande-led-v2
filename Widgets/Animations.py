import json

from PySide6.QtWidgets import QFileDialog

from Memory.Pressed import get_current_frame, get_saved_frames, set_saved_frames, set_current_frame, get_setup
from Colors.conversions import rgb_to_hex, hex_to_rgb


def indicate_page(window, savedFrames, currentFrame):
    """
    Affiche l'index de la page courante sur le nombre de pages totales
    """
    window.pageIndicator.setText(f"frame : {currentFrame + 1}/{len(savedFrames) + 1}")
    set_saved_frames(savedFrames)
    set_current_frame(currentFrame)


def clean_boxes(leds):
    """
    Met toutes les cases en blanc
    """
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
    if currentFrame == len(savedFrames) - 1:
        clean_boxes(leds)
    else:
        load_frame(savedFrames[currentFrame + 1], leds, window)
        display_frame(leds)
    currentFrame += 1
    indicate_page(window, savedFrames, currentFrame)


def change_frame(currentFrame, savedFrames, leds, window):
    """
    Gère la sauvegarde et la modification de frames en fonction de l'indice et de la longueur de la liste
    """
    try:
        if savedFrames[currentFrame][0] != -1:
            if currentFrame == len(savedFrames):
                save_frame(leds, savedFrames, window)
            else:
                modif_frame(leds, savedFrames, currentFrame, window)
    except IndexError:
        if currentFrame == len(savedFrames):
            save_frame(leds, savedFrames, window)
        else:
            modif_frame(leds, savedFrames, currentFrame, window)


def save(saveButton):
    """
    Sauvegarde un fichier d'animation
    """
    try:
        fileName = QFileDialog.getSaveFileName(saveButton, "Save animation", f"ressources\\setups\\{get_setup()}\\"
                                                                             f"uncompiled", "Json Files (*.json)")
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
    """
    Affiche la couleur des leds selon la liste "leds"
    """
    if leds[0].color != "anim":
        for led in leds:
            ledColor = hex_to_rgb(led.color)
            led.setStyleSheet(f"border-radius: 3px;"
                              f"border: 2px solid blue;"
                              f"outline: solid;"
                              f"background-color: rgb({ledColor[0]}, {ledColor[1]}, {ledColor[2]});")
    else:
        display_anim(leds)


def display_anim(leds):
    """
    Affiche une bordure verte autour de toutes les cases (représente une information)
    """
    for led in leds:
        led.setStyleSheet(f"border-radius: 3px;"
                          f"border: 2px solid green;"
                          f"outline: solid;"
                          f"background-color: white;")


def load_frame(frame, leds, window):
    """
    Charge une frame ou une animation sur l'affichage
    """
    if frame[0] != -1:
        window.timeChoose.setValue(frame[0])
        for i in range(0, len(leds)):
            leds[i].color = frame[i+1]
            leds[i].isLocked = True
    else:
        for i in range(1, len(leds)):
            leds[i-1].color = "anim"
            leds[i-1].isLocked = True


def load(window, loadButton, leds):
    """
    Charge un fichier d'animation
    """
    try:
        fileName = QFileDialog.getOpenFileName(loadButton, "Load animation", f"ressources\\setups\\{get_setup()}\\"
                                                                             f"uncompiled", "Json Files (*.json)")
        with open(fileName[0], "r") as file:
            set_saved_frames(json.load(file))
        set_current_frame(len(get_saved_frames()) - 1)
        next_frame(leds, window)
    except FileNotFoundError:
        pass


def suppress_frame(window, leds):
    """
    Supprime une frame de l'affichage et de la sauvegarde et retourne une frame en arrière
    """
    savedFrames = get_saved_frames()
    currentFrame = get_current_frame()
    try:
        savedFrames.pop(currentFrame)
        set_saved_frames(savedFrames)
        if currentFrame > 0:
            load_frame(savedFrames[currentFrame - 1], leds, window)
            display_frame(leds)
            currentFrame -= 1
            indicate_page(window, savedFrames, currentFrame)
    except IndexError:
        pass


def insert_animation(window, leds):
    """
    Permet de choisir et d'insérer une animation
    """
    try:
        fileName = QFileDialog.getOpenFileName(None, "Load animation", f"ressources\\setups\\{get_setup()}\\uncompiled",
                                               "Json Files (*.json)")
        with open(fileName[0], "r"):
            savedFrames = get_saved_frames()
            if len(savedFrames) == get_current_frame():
                savedFrames.append([-1, fileName[0]])
            else:
                savedFrames[get_current_frame()] = [-1, fileName[0]]
            for led in leds:
                led.isLocked = True
            next_frame(leds, window)
    except FileNotFoundError:
        pass
