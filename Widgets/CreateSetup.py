from functools import partial

import Widgets.loadSetup
from Widgets.setButtons import link_buttons


def generate_config(height, width):
    return [[1 for _ in range(width)] for _ in range(height)]


def save_config(name, config):
    with open(f"ressources/setups/{name}/{name}.txt", "w") as f:
        for i in config:
            for j in i:
                f.write(str(i[j]))
            f.write("\n")


def clean_setup_horiz(buttons):
    for line in range(len(buttons)):
        if sum(buttons[line]):
            break
        buttons.pop(line)
        print("pop")
    return buttons[::-1]


def clean_setup(buttonsGrid):
    buttons = clean_setup_horiz(buttonsGrid)
    return clean_setup_horiz(buttons)


def grid_to_string(grid):
    return '\n'.join([''.join([str(i) for i in grid[j]]) for j in range(len(grid))]) + '\n'


def save_buttons(name, grid, configurator, window):
    config = ""
    for i in configurator:
        for _ in i:
            config += str(int(grid.pop(0).isLocked))
        config += "\n"

    with open(f"ressources/setups/{name}/{name}.txt", "w") as f:
        f.write(config)

    leds = Widgets.loadSetup.load_setup(window, name)
    link_buttons(leds, window)


def save_setup(window, name, grid, configurator):
    window.saveButton.clicked.connect(partial(save_buttons, name, grid, configurator, window))


def incapacitate_buttons(window):
    buttons = [window.backButton, window.nextButton, window.saveButton, window.loadButton]
    for button in buttons:
        button.clicked.disconnect()


def display_creation_widget(window, name, sizeX, sizeY):
    configurator = generate_config(sizeY, sizeX)
    save_config(name, configurator)
    grid = Widgets.loadSetup.load_setup(window, name)
    save_setup(window, name, grid, configurator)
