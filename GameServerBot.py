import threading
import configparser
import logging
import time
import datetime
import signal, os

from ArkServerHandler import ArkServerHandler
from MinecraftServerHandler import MinecraftServerHandler

config = configparser.ConfigParser()

config.read('config.ini')

logging.basicConfig(format='%(asctime)s %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S',filename='bot.log', encoding='utf-8', level=logging.DEBUG)

logging.info("Démarrage du bot")

# Liste des serveurs 
servers = []

for server in config.sections():
    if (config[server]['type'] == 'MINECRAFT'):
        logging.info("Chargement d'un serveur {} (minecraft)".format(server))
        newserver = MinecraftServerHandler(name=server, host=config[server]['server'], password=config[server]['password'])
        servers.append(newserver)
        newserver.start()
    if (config[server]['type'] == 'ARK'):
        logging.info("Chargement d'un serveur {} (ARK)".format(server))
        newserver = ArkServerHandler(name=server, host=config[server]['server'], password=config[server]['password'])
        servers.append(newserver)
        newserver.start()
    time.sleep(5)

while True:
    try:     
        time.sleep(5)
        logging.debug("ALIVE")
        for server in servers:
            timediff=datetime.datetime.now() - server.last_update
            if timediff.seconds >= 15:
                logging.error("Aucune mise à jour de {} depuis plus de 30s {}".format(server.getName()))
                server.start()
            else:
                logging.debug("Dernière mise à jour de l'état du serveur {} : {}s".format(server.getName(), timediff.seconds))
    except (Exception) as err:
        logging.error("{}".format(err))
        pass

