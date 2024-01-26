from functools import partial

from Memory.Pressed import reset
from SSH.SSHCommands import launch_color, launch_hyperion, quit_hyperion
from Widgets.Animations import back_frame, next_frame, save, load, suppress_frame, insert_animation
from Widgets.ColorWidget import change_bg_sliders, change_bg_hex, change_bg_pantone, change_bg_spinbox
import Widgets.loadSetup


def link_buttons(leds, window):
    """
    Relie les boutons à leurs fonctions
    """
    window.backButton.clicked.connect(partial(back_frame, leds, window))
    window.nextButton.clicked.connect(partial(next_frame, leds, window))
    window.saveButton.clicked.connect(partial(save, window.saveButton))
    window.loadButton.clicked.connect(partial(load, window, window.loadButton, leds))


def setup_window(window, leds):
    """
    Affiche la fenêtre de base de l'application
    """
    window.setStyleSheet(f"background-color : black")

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

    changeSpin = partial(change_bg_spinbox, window)

    window.valRed.valueChanged.connect(changeSpin)
    window.valGreen.valueChanged.connect(changeSpin)
    window.valBlue.valueChanged.connect(changeSpin)
    window.editHexa.textChanged.connect(partial(change_bg_hex, window))
    window.editPantone.returnPressed.connect(partial(change_bg_pantone, window))

    window.colorLaunch.clicked.connect(partial(launch_color, window))
    window.launchHyperyon.clicked.connect(launch_hyperion)
    window.quitHyperyon.clicked.connect(quit_hyperion)

    link_buttons(leds, window)
    reset()

    window.suppressFrame.triggered.connect(partial(suppress_frame, window, leds))
    window.insertAnimation.triggered.connect(partial(insert_animation, window, leds))
    window.changeID.triggered.connect(partial(Widgets.loadSetup.choose_setup, window))
