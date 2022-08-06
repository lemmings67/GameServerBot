import threading
import re
import time
import logging
import json
import datetime
import configparser
from mcrcon import MCRcon

config = configparser.ConfigParser()

config.read('config.ini')

class GameServerHandler(MCRcon, threading.Thread):

    # Etat du serveur
    server_status="UNKOWN"
    # Dernière mise à jour 
    last_update=datetime.datetime.now()
    # Dernière modification 
    last_change=datetime.datetime.now()
    # Arrêt du serveur
    stopped=False
    # Liste des joueurs
    players=[]

    def __init__(self, name, host, password, port, tlsmode=0, timeout=5):
        super().__init__(host, password, port, tlsmode, timeout)
        self.server_name = name
        threading.Thread.__init__(self)

    # Mise à jour de l'état du serveur
    def update(self):
        server_dict = {
            'status': self.server_status,
            'last_update': self.last_update.isoformat(),
            'last_change': self.last_change.isoformat(),
            'connected_players': self.players
        }
        with open(config['DEFAULT']['webserver_root'] + self.server_name + '.json', 'w') as f:
            f.write(json.dumps(server_dict))

    # Mise à jour de la liste des joueurs 
    def setPlayers(self, new_players):
        if (self.players != new_players):
            self.players = new_players
            self.last_change = datetime.datetime.now()
            logging.info("{} - {} players connected: {}".format(self.server_name, len(self.players), self.players))
            self.update()

    # Mise à jour du status
    def setStatus(self, new_status):
        if (self.server_status != new_status):
            if new_status == "UP": 
                logging.info(f"{self.server_name} - Connexion au serveur établie")
            else:
                logging.info(f"{self.server_name} - Déconnexion du serveur")
            self.server_status=new_status
            self.last_update = datetime.datetime.now()
            logging.info(f"{self.server_name} - Status is {self.server_status}")
            self.update()

    def getName(self):
        return self.server_name

    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            try:
                self.last_update = datetime.datetime.now()
                if (self.server_status != "UP"):
                    logging.debug(f"{self.server_name} - Tentative de connexion au serveur {self.host}")
                    self.connect()
                    self.setStatus("UP")
                self.setPlayers(self.getPlayerList())
            except (Exception) as err:
                logging.debug(f"{self.server_name} - {err}")                
                self.setStatus("DOWN")
                self.players=[]
                self.disconnect()
            time.sleep(5)