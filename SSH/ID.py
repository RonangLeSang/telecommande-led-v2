
def get_id_from_text(content):
    return tuple(content.split("|"))


def get_id_from_file(file):
    try:
        with open(f"ressources\\setups\\{file}\\config.txt", "r") as f:
            content = f.read()
            return get_id_from_text(content)
    except FileNotFoundError:
        ip_address = "0.0.0.0"
        username = ""
        password = ""
        return tuple([ip_address, username, password])
