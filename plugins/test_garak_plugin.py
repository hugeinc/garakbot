import os
import sys
import garak
import unittest
from mock import Mock
from errbot.backends.test import testbot, push_message, pop_message
from errbot.plugin_manager import get_plugin_obj_by_name


class TestGarakPlugin(object):
    extra_plugin_dir = '.'
    random_quotes = [{'quote': 'First Quote!', 'attr': 'Garak Said That 1 Time'},
                     {'quote': 'Second Quote!', 'attr': 'Garak Said That 2 Times'},
                     {'quote': 'Third Quote!', 'attr': 'Garak Said That 3 Times'},
                     {'quote': 'Fourth Quote!', 'attr': 'Garak Said That 4 Times'},
                     {'quote': 'Fifth Quote!', 'attr': 'Garak Said That 5 Times'},
                     ]

    def test_plugin_has_methods(self, testbot):
        p = get_plugin_obj_by_name('GarakBot')
        assert p is not None

        assert hasattr(p, 'hello')
        assert hasattr(p, 'number44')
        assert hasattr(p, 'spock')
        assert hasattr(p, 'tellme_something')


    def test_mycommand_hello_returns_expected_output(self, testbot):
        push_message('! hello')
        assert "Hello. You're a killer, admit it. We both are.However, I'm also a very *good* tailor." in pop_message()

    def test_mycommand_number44_returns_expected_output(self, testbot):
        push_message('! number44')
        assert "WHOOOO! 44 THAT'S ME!! GETTING SOME COLD CUTS TODAY!!" in pop_message()

    def test_mycommand_spock_returns_expected_output(self, testbot):
        push_message('! spock')
        assert "Live Long and Prosper. - R.I.P Mr. Spock" in pop_message()

    def test_mycommand_tellme_something_returns_expected_output(self, testbot):
        p = get_plugin_obj_by_name('GarakBot')
        p.get_garak_quote_datasource = Mock()
        p.get_garak_quote_datasource.return_value = self.random_quotes

        push_message('! tellme something')
        assert 'Quote!' in pop_message()

    def test_mycommand_tellme_something_with_nodata_fails_gracefully(self, testbot):
        p = get_plugin_obj_by_name('GarakBot')
        p.get_garak_quote_datasource = Mock()
        p.get_garak_quote_datasource.return_value = None
        push_message('! tellme something')
        assert "I'm Sorry, I have nothing to say. For now." in pop_message()

    def test_mycommand_tellme_something_with_nodata_returns_random_output(self, testbot):
        p = get_plugin_obj_by_name('GarakBot')
        p.get_garak_quote_datasource = Mock()
        p.get_garak_quote_datasource.return_value = self.random_quotes

        push_message('! tellme something')
        a = pop_message()

        push_message('! tellme something')
        b = pop_message()

        assert a is not None
        assert b is not None
        assert a != b

        #Test Load_data by overriding config? need to change behavior to load dict from JSON string Instead of file

        # who are you? -> Oh, it's just Garak. Plain, simple Garak.
        # whats -> random quote
        # ds9 -> Random show/space station fact
        #happenings

