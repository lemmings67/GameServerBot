import configparser
import logging
import time

from ArkServerHandler import ArkServerHandler
from MinecraftServerHandler import MinecraftServerHandler

config = configparser.ConfigParser()

config.read('config.ini')

logging.basicConfig(format='%(asctime)s %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S',filename='bot.log', encoding='utf-8', level=logging.INFO)

logging.info("Démarrage du bot")

# Liste des serveurs 
servers = []

for server in config.sections():
    if (config[server]['type'] == 'MINECRAFT'):
        newserver = MinecraftServerHandler(host=config[server]['server'], password=config[server]['password'])
        servers.append(newserver)
        newserver.start()
    if (config[server]['type'] == 'ARK'):
        newserver = ArkServerHandler(host=config[server]['server'], password=config[server]['password'])
        servers.append(newserver)
        newserver.start()
    time.sleep(5)

    while True:     
        time.sleep(30)
