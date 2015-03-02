from errbot import BotPlugin, botcmd

class GarakBot(BotPlugin):
    """
    Obsidian Order Chat Robot
    """
    @botcmd
    def hello(self, msg, args):
        """Say hello to the world"""
        return "Hello, world!"

    @botcmd
    def get44(self,msg,args):
        return "44 THAT'S ME!! GET SOME COLD CUTS, GET SOME COLD CUTS,GET SOME COLD CUTS...GETTING SOME COLD CUTS TODAY!!"