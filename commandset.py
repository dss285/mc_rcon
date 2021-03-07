import mcrcon
import time
class CommandSet:
    def __init__(self, commands, delay, target, *args):
        self.args = args
        self.delay = delay
        self.target = target
        self.commands = commands
    def run(self,):
        rcon = mcrcon.RCON(*self.args)
        rcon.connect()
        for i in self.commands:
            rcon.command(i.format(target=self.target))
            time.sleep(self.delay)
        rcon.disconnect()
        return True