from errbot import BotPlugin, botcmd
import os, json
from random import choice
from io import StringIO
from config import GARAK_QUOTE_DATA
import logging

class GarakBot(BotPlugin):
    """
    Obsidian Order Chat Robot
    """
    def __init__(self, quote_data_src=None):
        super(GarakBot, self).__init__()
        self.garak_quote_ds = quote_data_src or os.path.abspath(GARAK_QUOTE_DATA)
        self.last_garak_quote = None

    @botcmd
    def hello(self, msg, args):
        """Just Say Hello"""
        return "Hello. You're a killer, admit it. We both are.However, I'm also a very *good* tailor."

    @botcmd
    def number_44(self, msg, args):
        """Call My Number. Am I next?"""
        return "WHOOOO! 44 THAT'S ME!! GETTING SOME COLD CUTS TODAY!!"

    @botcmd
    def spock(self, msg, args):
        """Give a tribute to a dear friend and leader"""
        return "Live Long and Prosper. - R.I.P Mr. Spock"

    @botcmd(template="quote")
    def tellme_something(self, msg, args):
        """Make Idle Chit Chat"""
        quote_store = self.get_garak_quote_datasource()
        if quote_store is None:
            return {"quote":"I'm Sorry, I have nothing to say. For now.", "attr":"Garak"}
        newquote = choice(quote_store)

        while self.last_garak_quote == newquote and len(quote_store) > 1:
            newquote = choice(quote_store)
        self.last_garak_quote = newquote
        return newquote

    def get_garak_quote_datasource(self):
        if not 'garak_quotes' in self or self['garak_quotes'] is None:
            self['garak_quotes'] = self.load_data_sources()
        return self['garak_quotes']

    def clear_garak_quote_datasource(self):
        try:
            del self['garak_quotes']
        except (KeyError, AttributeError):
            logging.error("Error Clearing Quote Data from shelf")

    def load_data_sources(self):
        if type(self.garak_quote_ds) == StringIO:
            try:
                return json.load(self.garak_quote_ds)
            except (IOError, ValueError):
                logging.error("Error Loading JSON value form StringIO")
        if type(self.garak_quote_ds) == str:
            try:
                return json.load(open(self.garak_quote_ds))
            except (IOError, ValueError):
                logging.error("Error Loading JSON value form file")
        return None

