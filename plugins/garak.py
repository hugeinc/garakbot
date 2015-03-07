import logging
from errbot import BotPlugin, botcmd
import os, json
from random import choice
from io import StringIO
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
    def __init__(self, quote_data_src=None):
        super(GarakBot, self).__init__()
        self.garak_quote_ds = quote_data_src or os.path.abspath(GARAK_QUOTE_DATA)
        self.last_garak_quote = None

    @botcmd
    def hello(self, msg, args):
        """Say hello to the world"""
        return "Hello. You're a killer, admit it. We both are.However, I'm also a very *good* tailor."

    @botcmd
    def number_44(self, msg, args):
        return "WHOOOO! 44 THAT'S ME!! GETTING SOME COLD CUTS TODAY!!"

    @botcmd
    def spock(self, msg, args):
        return "Live Long and Prosper. - R.I.P Mr. Spock"

    @botcmd(template="quote")
    def tellme_something(self, msg, args):
        quote_store = self.get_garak_quote_datasource()
        if quote_store is None:
            return {"quote":"I'm Sorry, I have nothing to say. For now.", "attr":"Garak"}
        newquote = choice(quote_store)
        while self.last_garak_quote == newquote:
            newquote = choice(quote_store)
        self.last_garak_quote = newquote
        return newquote

    def get_garak_quote_datasource(self):
        if not 'garak_quotes' in self or self['garak_quotes'] is None:
           self['garak_quotes'] = self.load_data_sources()
        return self['garak_quotes']

    def load_data_sources(self):
        if type(self.garak_quote_ds) == StringIO:
            try:
                return json.load(self.garak_quote_ds)
            except (IOError, ValueError):
                pass
        if type(self.garak_quote_ds) == str:
            try:
                return json.load(open(self.garak_quote_ds))
            except (IOError, ValueError):
                pass
        return None

