import Widgets.loadSetup


def generate_config(height, width):
    return [[1 for i in range(width)] for j in range(height)]


def save_config(name, config):
    with open(f"ressources/setups/{name}/{name}.txt", "w") as f:
        for i in config:
            for j in i:
                f.write(str(i[j]))
            f.write("\n")


def save_setup(window):
    window


def incapacitate_buttons(window):
    buttons = [window.backButton, window.nextButton, window.saveButton, window.loadButton]
    for button in buttons:
        button.clicked.disconnect()


def display_creation_widget(window, name, sizeX, sizeY):
    save_config("config", generate_config(sizeX, sizeY))
    Widgets.loadSetup.load_setup(window, "config")
    incapacitate_buttons(window)
