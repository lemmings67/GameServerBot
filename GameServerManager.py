#!/usr/bin/python3

import configparser
import logging
import time
import sys
import os

from ArkServerHandler import ArkServerHandler
from MinecraftServerHandler import MinecraftServerHandler

config = configparser.ConfigParser()

config.read('config.ini')

logging.basicConfig(format='%(asctime)s %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S',filename='bot.log', encoding='utf-8', level=logging.INFO)

servername = sys.argv[1]
cmd_opt = sys.argv[2]
server = ""


def notify_stop_server():
    server.connect()
    for countdown in range(60):
        timer = 60-countdown
        if (timer % 10) == 0 or timer < 10: 
            print("Arret du serveur dans : {}s".format(timer))
            server.sendMessage("Arret du serveur dans {}s".format(timer))
        time.sleep(1)
    print("Arret du serveur IMMEDIAT !!!")
    server.sendMessage("Arret du serveur IMMEDIAT !!!")


def execute_cmd(cmd, cmd_opt):
    print("Commande: ", cmd + ' ' + cmd_opt)
    if cmd_opt == 'stop':
        notify_stop_server()
    stream = os.popen(cmd + ' ' + cmd_opt)
    output = stream.read()
    return 0

if (cmd_opt != None):
    if config.has_section(servername):
        print("Server: ", servername)

        if (config[servername]['type'] == 'MINECRAFT'):
            server = MinecraftServerHandler(host=config[servername]['server'], password=config[servername]['password'])
        if (config[servername]['type'] == 'ARK'):
            server = ArkServerHandler(host=config[servername]['server'], password=config[servername]['password'])

        lsgm_cmd = config[servername]['lsgm_cmd']        
        execute_cmd(lsgm_cmd, cmd_opt)

    else:
        print("No server : ", servername)