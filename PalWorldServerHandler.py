import threading
import re
import time
import logging
from mcrcon import MCRcon

from GameServerHandler import GameServerHandler

class PalWorldServerHandler(GameServerHandler):

    def __init__(self, name, host, password, port=25575, tlsmode=0, timeout=5):
        super().__init__(name, host, password, port, tlsmode, timeout)

    def getPlayerList(self):
        result = self.command('ShowPlayers')
        logging.debug(f"{self.host} <---- \n{result}")
        output=[]
        tmp = result.splitlines()
        for line in tmp:
            if not re.match('name,playeruid,steamid', line):
                if re.match('.*,.*,.*',line):
                    output.append(line.split(',')[0])
        return output

    def sendMessage(self, message):
        return self.command(message)


