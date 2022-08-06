import re
import logging

from GameServerHandler import GameServerHandler

class MinecraftServerHandler(GameServerHandler):

    def __init__(self, host, password, port=25575, tlsmode=0, timeout=5):
        super().__init__(host, password, port, tlsmode, timeout)

    def run_command(self, command):
        try:
            return self.command(command)
        except Exception as e:
            logging.debug("{self.host} <---- \n{output}")
            return ""

    def getPlayerList(self):

        self.run_command("/list")
        
        logging.debug(f"{self.host} <---- \n{output}")
        output = re.sub('.*: ','',output)
        output = re.sub(' ', '', output)
        
        if output=='':
            return []
        
        return output.split(',')

    def sendMessage(self, message):
        return self.run_command("/say " + message)




