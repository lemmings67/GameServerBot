import threading
import re
import time
import logging
from mcrcon import MCRcon

from GameServerHandler import GameServerHandler

class ArkServerAHandler(GameServerHandler):

    def __init__(self, name, host, password, port=32330, tlsmode=0, timeout=5):
        super().__init__(name, host, password, port, tlsmode, timeout)

    def getPlayerList(self):
        result = self.command('ListPlayers')
        logging.debug(f"{self.host} <---- \n{result}")
        if re.search('Keep Alive', result):
            return self.players
        output=[]
        tmp = result.splitlines()
        for line in tmp:
            if re.match('[0-9]\..*, .*',line):
                output.append(re.sub('[0-9]. ', '', re.sub(', .*$', '', line)))
        return output

    def sendMessage(self, message):
        return self.command('ServerChat ' + message)


