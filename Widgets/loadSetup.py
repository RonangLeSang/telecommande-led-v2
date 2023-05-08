from Memory.Pressed import set_setup
from Widgets.ColorButton import ColorButton
from Widgets.changeSetup import display_form


def get_position(setup):
    return get_buttons([(line, row) for line in range(len(setup)-1) for row in range(len(setup[0]))], setup)


def get_buttons(positions, setup):
    return [[position, bool(int(setup[position[0]][position[1]]))] for position in positions]


def setup_grid(positions, sliderR, sliderG, sliderB, window):
    buttonsList = []
    for position in positions:
        if position[1]:
            button = ColorButton(sliderR, sliderG, sliderB)
            buttonsList.append(button)
            window.buttonLayout.addWidget(button, position[0][0], position[0][1])
    return buttonsList


def get_last_setup():
    with open("ressources\\setups\\save.txt", "r") as f:
        return f.read()


def set_last_setup(setup):
    set_setup(setup)
    with open("ressources\\setups\\save.txt", "w") as f:
        return f.write(setup)


def load_setup(window=None, file=False):
    clear_setup(window)
    if not file:
        file = get_last_setup()
    set_last_setup(file)
    setup = []
    with open(f"ressources\\setups\\{file}\\{file}.txt", "r") as f:
        line = f"foo"
        while line != "":
            line = f.readline()
            setup.append(line[:-1])
    return setup_grid(get_position(setup), window.sliderRed, window.sliderGreen, window.sliderBlue, window)


def clear_setup(window):
    for i in reversed(range(window.buttonLayout.count())):
        window.buttonLayout.itemAt(i).widget().setParent(None)


def load_from_combo(window, combo):
    load_setup(window, combo.currentText())


def choose_setup(window):
    clear_setup(window)
    display_form(window)
