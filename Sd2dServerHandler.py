import threading
import re
import time
import logging
import datetime
import json
import configparser

import telnetlib

config = configparser.ConfigParser()

config.read('config.ini')


class Sd2dServerHandler(threading.Thread):

    # Server
    tn = telnetlib.Telnet()

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

    def __init__(self, name, host, password, port=8081, timeout=5):
        self.host = host
        self.port = port
        self.password = password
        self.timeout = timeout
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

    def getPlayerList(self):
        self.sendMessage('ListPlayers')
        result = self.read_until('Total')
        logging.debug(f"{self.host} <---- \n{result}")
        output=[]
        tmp = result.splitlines()
        for line in tmp:
            if re.match('[0-9]\..*, .*',line):
                output.append(re.sub('[0-9]. ', '', re.sub(', .*$', '', line)))
        return output

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

    # Mise à jour de la liste des joueurs 
    def setPlayers(self, new_players):
        if (self.players != new_players):
            self.players = new_players
            self.last_change = datetime.datetime.now()
            logging.info("{} - {} players connected: {}".format(self.server_name, len(self.players), self.players))
            self.update()

    def sendMessage(self, message):
        #logging.debug(f"{self.host}:{self.port} >>> " + message)
        return self.tn.write(message.encode('ascii')+ b"\n")

    def getName(self):
        return self.server_name

    def stop(self):
        self.stopped = True

    def read(self):
        # Lire jusqu'à ce que l'invite attendue soit trouvée
        response = self.tn.read_eager()

        # Retourner la réponse décodée
        return response.decode('ascii')
    
    def read_until(self, expected):
        # Lire jusqu'à ce que l'invite attendue soit trouvée
        response = self.tn.read_until(expected.encode('ascii'), timeout=self.timeout)
        #logging.debug(f"{self.host}:{self.port} <<< " + response)
        # Retourner la réponse décodée
        return response.decode('ascii')
        
    def run(self):
        while not self.stopped:
            try:
                self.last_update = datetime.datetime.now()
                if (self.server_status != "UP"):
                    logging.info(f"{self.server_name} - Tentative de connexion au serveur {self.host}")
                    self.tn.open(self.host, self.port, self.timeout)
                    input = self.read_until('enter password:')
                    if (re.search('enter password:', input)):
                        self.sendMessage(self.password)
                    input = self.read_until('Connected with')
                    if (re.search('enter password:', input)):
                        logging.info(f"{self.server_name} - Connexion opérationnelle")
                    self.setStatus("UP")
                self.setPlayers(self.getPlayerList())
            except (Exception) as err:
                logging.error(f"{self.server_name} - {err}")                
                self.setStatus("DOWN")
                self.players=[]
                self.tn.close()
            time.sleep(5)
