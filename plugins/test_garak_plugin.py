import os
import sys
import garak
import unittest

from errbot.backends.test import testbot, push_message, pop_message
from errbot.plugin_manager import get_plugin_obj_by_name


class TestGarakPlugin(object):
    extra_plugin_dir = '.'

    def test_plugin_methods(self, testbot):
        p = get_plugin_obj_by_name('GarakBot')
        assert p is not None

        assert hasattr(p, 'hello')
        assert hasattr(p, 'number44')
        assert hasattr(p, 'spock')

    def test_mycommand_hello(self, testbot):
        push_message('! hello')
        assert "Hello. You're a killer, admit it. We both are.However, I'm also a very *good* tailor." in pop_message()

    def test_mycommand_number44(self, testbot):
        push_message('! number44')
        assert "WHOOOO! 44 THAT'S ME!! GETTING SOME COLD CUTS TODAY!!" in pop_message()

    def test_mycommand_spock(self, testbot):
        push_message('! spock')
        assert "Live Long and Prosper. - R.I.P Mr. Spock" in pop_message()


    # say what -> random quote
    # ds9 -> Random show/space station fact
    # spok -> "
    #happenings

