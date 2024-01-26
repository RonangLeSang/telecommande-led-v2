from Memory.Pressed import set_setup, set_ids_connection, reset
from SSH.ID import get_id_from_file
from Widgets.ColorButton import ColorButton
from Widgets.changeSetup import display_form
from Widgets.setButtons import link_buttons


def get_position(setup):
    """
    Récupère la position des cases depuis une liste
    """
    return get_buttons([(line, row) for line in range(len(setup)-1) for row in range(len(setup[0]))], setup)


def get_buttons(positions, setup):
    """
    Renvoi une liste de booléens représentant le setup
    """
    return [[position, bool(int(setup[position[0]][position[1]]))] for position in positions]


def setup_grid(positions, sliderR, sliderG, sliderB, window):
    """
    Place les boutons sur l'affichage
    """
    buttonsList = []
    for position in positions:
        if position[1]:
            button = ColorButton(sliderR, sliderG, sliderB)
            buttonsList.append(button)
            window.buttonLayout.addWidget(button, position[0][0], position[0][1])
    return buttonsList


def get_last_setup():
    """
    Récupère le dernier setup chargé depuis une sauvegarde
    """
    with open("ressources\\setups\\save.txt", "r") as f:
        return f.read()


def set_last_setup(setup):
    """
    Sauvegarde le nom du dernier setup chargé
    """
    set_setup(setup)
    with open("ressources\\setups\\save.txt", "w") as f:
        return f.write(setup)


def load_setup(window=None, file=False):
    """
    Charge un setup depuis un nom de fichier
    """
    clear_setup(window)
    if not file:
        file = get_last_setup()
        try:
            with open(f"ressources\\setups\\{file}\\{file}.txt", "r") as _:
                pass
        except FileNotFoundError:
            file = "default"
    if file == "config":
        set_last_setup("default")
    else:
        set_last_setup(file)
    setup = []
    with open(f"ressources\\setups\\{file}\\{file}.txt", "r") as f:
        line = f"foo"
        while line != "":
            line = f.readline()
            setup.append(line[:-1])
    return setup_grid(get_position(setup), window.sliderRed, window.sliderGreen, window.sliderBlue, window)


def clear_setup(window):
    """
    Supprime de l'affichage tous les boutons
    """
    for i in reversed(range(window.buttonLayout.count())):
        window.buttonLayout.itemAt(i).widget().setParent(None)


def load_from_combo(window, combo):
    """
    Charge un setup depuis le combo box de choix
    """
    leds = load_setup(window, combo.currentText())
    set_ids_connection(get_id_from_file(get_last_setup()))
    link_buttons(leds, window)
    reset()


def choose_setup(window):
    """
    Affiche la sous-fenêtre de choix de setup
    """
    clear_setup(window)
    display_form(window)
