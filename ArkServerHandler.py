import threading
import re
import time
import logging
from mcrcon import MCRcon

from GameServerHandler import GameServerHandler

class ArkServerHandler(GameServerHandler):

    def __init__(self, host, password, port=27020, tlsmode=0, timeout=5):
        super().__init__(host, password, port, tlsmode, timeout)

    def getPlayerList(self):
        result = self.command('ListPlayers')
        logging.debug("{self.host} <---- \n{result}")
        if re.search('Keep Alive', result):
            return self.players
        
        return [
            re.sub('[0-9]. ', '', re.sub(', .*$', '', line))
            for line in
                result.splitlines()
            if re.match('[0-9]\..*, .*',line)
        ]

    def sendMessage(self, message):
        return self.command('ServerChat ' + message)


