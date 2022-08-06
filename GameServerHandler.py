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

    def __init__(self, host, password, port, tlsmode=0, timeout=5):
        super().__init__(host, password, port, tlsmode, timeout)
        threading.Thread.__init__(self)

    # Mise à jour de l'état du serveur
    def update(self):
        server_dict = {
            'status': self.server_status,
            'last_update': self.last_update.isoformat(),
            'last_change': self.last_change.isoformat(),
            'connected_players': self.players
        }
        with open(config['DEFAULT']['webserver_root'] + self.host + '.json', 'w') as f:
            f.write(json.dumps(server_dict))

    # Mise à jour de la liste des joueurs 
    def setPlayers(self, new_players):
        if (self.players != new_players):
            self.players = new_players
            self.last_change = datetime.datetime.now()
            logging.info("{} - {} players connected: {}".format(self.host, len(self.players), self.players))
            self.update()

    # Mise à jour du status
    def setStatus(self, new_status):
        if (self.server_status != new_status):
            if new_status == "UP": 
                logging.info("{self.host} - Connexion au serveur établie")
            else:
                logging.info(f"{self.host} - Déconnexion du serveur")
            self.server_status=new_status
            self.last_update = datetime.datetime.now()
            logging.info(f"{self.host} - Status is {self.server_status}")
            self.update()

    def run(self):
        while not self.stopped:
            try:
                if (self.server_status != "UP"):
                    logging.debug(f"{self.host} - Tentative de connexion au serveur")
                    self.connect()
                    self.setStatus("UP")
                self.setPlayers(self.getPlayerList())
            except (Exception) as err:
                logging.debug(f"{self.host} - {err}")                
                self.setStatus("DOWN")
                self.players=[]
                self.disconnect()
            time.sleep(5)