import os
import Widgets.loadSetup

from functools import partial

from PySide6.QtWidgets import QWidget, QComboBox, QPushButton, QLineEdit, QLabel, QHBoxLayout, QVBoxLayout, QSpinBox

from Widgets.CreateSetup import display_creation_widget, incapacitate_buttons


def display_form(window):
    incapacitate_buttons(window)
    formScreen = QWidget()
    comboSetup = QComboBox()
    spinHoriz = QSpinBox()
    spinVert = QSpinBox()
    chooseButton = QPushButton("confirmer")
    nameField = QLineEdit()
    ipField = QLineEdit()
    loginField = QLineEdit()
    passwordField = QLineEdit()
    nameLabel = QLabel("nom de la configuration")
    ipLabel = QLabel("IP")
    loginLabel = QLabel("identifiant")
    passwordLabel = QLabel("mot de passe")
    createButton = QPushButton("créer")
    cancelButton = QPushButton("annuler")
    labelSpinHoriz = QLabel("taille x :")
    labelSpinVert = QLabel("taille y :")

    nameField.setFixedWidth(500)
    ipField.setFixedWidth(500)
    loginField.setFixedWidth(500)
    passwordField.setFixedWidth(500)
    formScreen.setStyleSheet(f"background-color : grey")

    folders = next(os.walk('ressources/setups'))[1]
    for folder in folders:
        comboSetup.addItem(folder)

    cancelButton.clicked.connect(partial(Widgets.loadSetup.load_setup, window))
    chooseButton.clicked.connect(partial(Widgets.loadSetup.load_from_combo, window, comboSetup))
    createButton.clicked.connect(partial(create_setup, window, nameField, ipField, loginField, passwordField, spinHoriz, spinVert))

    nameLayout = QHBoxLayout()
    ipLayout = QHBoxLayout()
    loginLayout = QHBoxLayout()
    passwordLayout = QHBoxLayout()
    sizeLayout = QHBoxLayout()
    formLayout = QVBoxLayout()
    chooseLayout = QVBoxLayout()
    createLayout = QVBoxLayout()
    chooseCreateLayout = QHBoxLayout()

    formScreen.setLayout(formLayout)
    createLayout.addLayout(nameLayout)
    createLayout.addLayout(ipLayout)
    createLayout.addLayout(loginLayout)
    createLayout.addLayout(passwordLayout)
    createLayout.addLayout(sizeLayout)
    chooseCreateLayout.addLayout(chooseLayout)
    chooseCreateLayout.addLayout(createLayout)
    formLayout.addLayout(chooseCreateLayout)

    sizeLayout.addWidget(labelSpinHoriz)
    sizeLayout.addWidget(spinHoriz)
    sizeLayout.addWidget(labelSpinVert)
    sizeLayout.addWidget(spinVert)
    nameLayout.addWidget(nameLabel)
    nameLayout.addWidget(nameField)
    ipLayout.addWidget(ipLabel)
    ipLayout.addWidget(ipField)
    loginLayout.addWidget(loginLabel)
    loginLayout.addWidget(loginField)
    passwordLayout.addWidget(passwordLabel)
    passwordLayout.addWidget(passwordField)
    chooseLayout.addWidget(comboSetup)
    chooseLayout.addWidget(chooseButton)
    createLayout.addWidget(createButton)
    formLayout.addWidget(cancelButton)
    window.buttonLayout.addWidget(formScreen, 0, 0)


def create_setup(window, nameField, ipField, loginField, passwordField, spinHoriz, spinVert):
    try:
        os.makedirs(f"ressources/setups/{nameField.text()}/compiled")
        os.mkdir(f"ressources/setups/{nameField.text()}/uncompiled")
        with open(f"ressources/setups/{nameField.text()}/config.txt", "w") as file:
            file.write(f"{ipField.text()}|{loginField.text()}|{passwordField.text()}")
        display_creation_widget(window, nameField.text(), spinHoriz.value(), spinVert.value())

    except FileExistsError:
        pass
