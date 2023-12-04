import threading
import time

import paramiko

from Memory.Pressed import set_ssh_client


class ConnectionAttempt(threading.Thread):
    """
    Thread qui tente de se connecter au raspberry
    """

    def __init__(self, IDs, window):
        threading.Thread.__init__(self)
        self.isConnected = False
        self.ip_address = IDs[0]
        self.username = IDs[1]
        self.password = IDs[2]
        self.window = window

    def set_ids(self, IDs):
        self.ip_address = IDs[0]
        self.username = IDs[1]
        self.password = IDs[2]

    def run(self):
        """
        Continue d'essayer de se connecter tant qu'il n'y arrive pas et marque de courtes pauses
        """
        while not self.isConnected or self.ip_address != "0.0.0.0":
            connectionWait = ConnectionWait(self.window)
            connectionWait.start()
            if not connect(self.ip_address, self.username, self.password, connectionWait, self.window):
                time.sleep(5)
            else:
                self.isConnected = True
            connectionWait.stop = True
            connectionWait.join()


class ConnectionWait(threading.Thread):
    """
    affiche un visuel d'attente de connection
    """

    def __init__(self, window):
        threading.Thread.__init__(self)
        self.stop = False
        self.window = window

    def run(self):
        """
        Affiche un visuel jusqu'à la connection
        """
        time.sleep(2)
        i = 0
        while not self.stop:
            wait_connection(i, self.window)
            time.sleep(0.2)
            if i == 3:
                i = 0
            else:
                i += 1


def connect(ip_address, username, password, connectionWait, window):
    """
    Tente une connection en SSH en renvoie l'état de connection
    :param window:
    :param ip_address:
    :param username:
    :param password:
    :param connectionWait:
    :return: l'état de connection
    """
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    set_ssh_client(ssh_client)
    try:
        ssh_client.connect(hostname=ip_address, username=username, password=password)
        ssh_client.invoke_shell()
        connectionWait.stop = True
        connectionWait.join()
        connected(ip_address, window)
        return True
    except:
        connectionWait.stop = True
        connectionWait.join()
        not_connected(window)
        return False


def connected(ip_address, window):
    """
    Affiche la réussite de connection sur l'écran
    """
    window.connectionStatus.setText(f"connecté à : {ip_address}")


def not_connected(window):
    """
    Affiche l'échec de connection sur l'écran
    """
    window.connectionStatus.setText("échec de la connection")


def wait_connection(i, window):
    """
    Affiche l'attente de connection en fonction de l'indice
    """
    affichage = ["En attente de connexion   ", "En attente de connexion.  ", "En attente de connexion.. ",
                 "En attente de connexion..."]
    window.connectionStatus.setText(affichage[i])
