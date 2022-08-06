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

logging.basicConfig(format='%(asctime)s %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S',filename='bot.log', encoding='utf-8', level=logging.INFO)

logging.info("Démarrage du bot")

# Liste des serveurs 
servers = []

def init_server(name):
    if (config[name]['type'] == 'MINECRAFT'):
        logging.info(f"Chargement d'un serveur {name} (minecraft)")
        newserver = MinecraftServerHandler(name=name, host=config[name]['server'], password=config[name]['password'])
        servers.append(newserver)
        newserver.start()
        return newserver
    if (config[name]['type'] == 'ARK'):
        logging.info(f"Chargement d'un serveur {name} (ARK)")
        newserver = ArkServerHandler(name=name, host=config[name]['server'], password=config[name]['password'])
        servers.append(newserver)
        newserver.start()
        return newserver
    return

# Initialisation de l'ensemble des serveurs
for server_name in config.sections():
    init_server(server_name)

# Boucle de watchdog des serveurs
while True:
    try:     
        time.sleep(15)
        logging.debug("ALIVE")
        for server in servers:
            timediff=datetime.datetime.now() - server.last_update
            if timediff.seconds >= 15:
                # Le thread de l'un des serveurs est mort (timeout)
                failed_server = server.getName()
                logging.error("Aucune mise à jour de {} depuis plus de 30s ".format(failed_server))
                server.stop()
                servers.remove(server)
                newserver=init_server(failed_server)
                newserver.start()
            else:
                # Tout va bien
                logging.debug("Dernière mise à jour de l'état du serveur {} : {}s".format(server.getName(), timediff.seconds))
    except (Exception) as err:
        logging.error("{}".format(err))
        pass

