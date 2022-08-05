import threading
import re
import time
import logging
from mcrcon import MCRcon

from GameServerHandler import GameServerHandler

class MinecraftServerHandler(GameServerHandler):

    def __init__(self, host, password, port=25575, tlsmode=0, timeout=5):
        super().__init__(host, password, port, tlsmode, timeout)

    def getPlayerList(self):
        output = self.command("/list")
        logging.debug("{} <---- \n{}".format(self.host, output))
        output = re.sub('.*: ','',output)
        output = re.sub(' ', '', output)
        if output=='':
            return []
        return output.split(',')

    def sendMessage(self, message):
        return self.command("/say " + message)




