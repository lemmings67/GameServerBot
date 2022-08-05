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
        result = self.con.command('ListPlayers')
        logging.debug("{} <---- \n{}".format(self.host, result))
        if re.search('Keep Alive', result):
            return self.players
        output=[]
        tmp = result.splitlines()
        for line in tmp:
            if re.match('[0-9]\..*, .*',line):
                output.append(re.sub('[0-9]. ', '', re.sub(', .*$', '', line)))
        return output

    def sendMessage(self, message):
        return sself.con.command('ServerChat ' + message)


