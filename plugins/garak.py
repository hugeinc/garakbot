from errbot import BotPlugin, botcmd


class GarakBot(BotPlugin):
    """
    Obsidian Order Chat Robot
    Store items transparently via mixin:
    self[title] = poll
    del self[title]
    List items:
    self.keys()
    """
    @botcmd
    def hello(self, msg, args):
        """Say hello to the world"""
        return "Hello. You're a killer, admit it. We both are.However, I'm also a very *good* tailor."

    @botcmd
    def number44(self,msg,args):
        return "WHOOOO! 44 THAT'S ME!! GETTING SOME COLD CUTS TODAY!!"

    @botcmd
    def spock(self,msg,args):
        return "Live Long and Prosper. - R.I.P Mr. Spock"