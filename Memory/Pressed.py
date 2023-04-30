global isPressed
global currentFrame
global savedFrames
global ssh_client
global setup
currentFrame = 0
savedFrames = []
isPressed = False


def switch_is_pressed():
    global isPressed
    isPressed = not isPressed


def get_is_pressed():
    global isPressed
    return isPressed


def set_ssh_client(client):
    global ssh_client
    ssh_client = client


def get_ssh_client():
    global ssh_client
    return ssh_client


def set_current_frame(curr):
    global currentFrame
    currentFrame = curr


def get_current_frame():
    global currentFrame
    return currentFrame


def set_saved_frames(savedF):
    global savedFrames
    savedFrames = savedF


def get_saved_frames():
    global savedFrames
    return savedFrames


def set_setup(newSetup):
    global setup
    setup = newSetup


def get_setup():
    global setup
    return setup
