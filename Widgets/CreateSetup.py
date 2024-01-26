from functools import partial

import Widgets.loadSetup
from Memory.Pressed import reset
from Widgets.setButtons import link_buttons


def generate_config(height, width):
    """
    Génère un setup de configuration (rectangle)
    """
    return [[1 for _ in range(width)] for _ in range(height)]


def save_config(name, config):
    """
    sauvegarde la configuration
    """
    with open(f"ressources/setups/{name}/{name}.txt", "w") as f:
        for i in config:
            for j in i:
                f.write(str(i[j]))
            f.write("\n")


def clean_setup_horiz(buttons):
    """
    Lors de l'enregistrement, enlève les lignes horizontales en trop
    """
    for line in range(len(buttons)):
        if sum(buttons[line]):
            break
        buttons.pop(line)
        print("pop")
    return buttons[::-1]


def clean_setup(buttonsGrid):
    """
    Lors de l'enregistrement, enlève les lignes en trop
    """
    buttons = clean_setup_horiz(buttonsGrid)
    return clean_setup_horiz(buttons)


def grid_to_string(grid):
    """
    Transforme une grille en string pour pouvoir l'enregistrer
    """
    return '\n'.join([''.join([str(i) for i in grid[j]]) for j in range(len(grid))]) + '\n'


def save_buttons(name, grid, configurator, window):
    """
    Sauvegarde la configuration à l'endroit donné
    """
    config = ""
    for i in configurator:
        for _ in i:
            config += str(int(grid.pop(0).isLocked))
        config += "\n"

    with open(f"ressources/setups/{name}/{name}.txt", "w") as f:
        f.write(config)

    leds = Widgets.loadSetup.load_setup(window, name)
    link_buttons(leds, window)
    reset()


def save_setup(window, name, grid, configurator):
    """
    Sauvegarde le sétup avec la configuration des boutons et les identifiants
    """
    window.saveButton.clicked.connect(partial(save_buttons, name, grid, configurator, window))


def incapacitate_buttons(window):
    """
    Enlève les fonctions de tous les boutons
    """
    buttons = [window.backButton, window.nextButton, window.saveButton, window.loadButton]
    try:
        for button in buttons:
            button.clicked.disconnect()
    except:
        pass


def display_creation_widget(window, name, sizeX, sizeY):
    """
    Affiche la grille de création de setup
    """
    configurator = generate_config(sizeY, sizeX)
    save_config(name, configurator)
    grid = Widgets.loadSetup.load_setup(window, name)
    save_setup(window, name, grid, configurator)
