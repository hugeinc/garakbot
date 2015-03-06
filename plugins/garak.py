from errbot import BotPlugin, botcmd
import os, json
from random import choice
from config import GARAK_QUOTE_DATA

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
    def number44(self, msg, args):
        return "WHOOOO! 44 THAT'S ME!! GETTING SOME COLD CUTS TODAY!!"

    @botcmd
    def spock(self, msg, args):
        return "Live Long and Prosper. - R.I.P Mr. Spock"

    @botcmd
    def tellme_something(self, msg, args):
        quoteStore = self.get_garak_quote_datasource()
        if quoteStore is None:
            return "I'm Sorry, I have nothing to say. For now."
        return choice(quoteStore)

    def get_garak_quote_datasource(self):
        if not 'garak_quotes' in self:
            self._load_data()

        return self['garak_quotes']

    def _load_data(self):
        '''
        SOOO HERE'S WHAT WE NEED TO DO:
        - READ DATA SOURCE FOR GARAK QUOTES FROM CONFIG INJECTED PATH
        - STORE DATA SOURCE IN DB (E.G. SELF, IN)
        -
        [{'quote': 'First This..', 'attr': 'Garak Said That 1 Time'},
                {'quote': 'Then That..', 'attr': 'Garak Said That 2 Times'}]

        '''
        qd = json.load(open(os.path.abspath(GARAK_QUOTE_DATA)))
        self['garak_quotes'] = qd
        return qd
