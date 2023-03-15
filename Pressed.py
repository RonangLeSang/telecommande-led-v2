global isPressed
isPressed = False


def switch_is_pressed():
    global isPressed
    isPressed = not isPressed


def get_is_pressed():
    global isPressed
    return isPressed
