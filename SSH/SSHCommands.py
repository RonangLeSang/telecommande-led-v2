from Memory.Pressed import get_ssh_client


def launch_color(window):
    """
    Quitte Hyperion et envoi la couleur choisi dans un fichier par SSH
    """
    quit_hyperion()
    ssh_client = get_ssh_client()
    chaine = f"echo {window.valRed.value()}l>/home/pi/coucou.txt"
    stdin, stdout, stderr = ssh_client.exec_command(chaine)
    chaine = f"echo {window.valGreen.value()}l>>/home/pi/coucou.txt"
    stdin, stdout, stderr = ssh_client.exec_command(chaine)
    chaine = f"echo {window.valBlue.value()}l>>/home/pi/coucou.txt"
    stdin, stdout, stderr = ssh_client.exec_command(chaine)
    stdin, stdout, stderr = ssh_client.exec_command("python3 /home/pi/hue.py")


def launch_hyperion():
    """
    Lance Hyperion par SSH
    """
    ssh_client = get_ssh_client()
    stdin, stdout, stderr = ssh_client.exec_command("/usr/bin/hyperiond")


def quit_hyperion():
    """
    Quitte Hyperion par SSH
    """
    ssh_client = get_ssh_client()
    stdin, stdout, stderr = ssh_client.exec_command("killall hyperiond")
