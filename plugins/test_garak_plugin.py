import os
import sys
import logging
import json
from io import StringIO
from errbot.backends.test import push_message, pop_message, FullStackTest
from errbot.plugin_manager import get_plugin_obj_by_name

config_module = sys.modules['errbot.config-template']
from tempfile import mkdtemp,NamedTemporaryFile
tempdir = mkdtemp(prefix='/tmp/')
config_module.BOT_DATA_DIR = tempdir
config_module.BOT_LOG_FILE = tempdir + os.sep + 'log.txt'
config_module.BOT_EXTRA_PLUGIN_DIR = []
config_module.BOT_LOG_LEVEL = logging.DEBUG
config_module.GARAK_QUOTE_DATA = '.'
sys.modules['config'] = config_module
from garak import GarakBot


class TestGarakPlugin(FullStackTest):
    extra_plugin_dir = '.'
    random_quotes = [{"quote": "First Quote!", "attr": "Garak Said That 1 Time(s)"},
                     {"quote": "Second Quote!", "attr": "Garak Said That 2 Time(s)"},
                     {"quote": "Third Quote!", "attr": "Garak Said That 3 Time(s)"},
                     {"quote": "Fourth Quote!", "attr": "Garak Said That 4 Time(s)"},
                     {"quote": "Fifth Quote!", "attr": "Garak Said That 5 Time(s)"},
    ]

    random_quotes2 = [k for k in random_quotes if k["quote"].startswith('F')]

    def setUp(self, extra_plugin_dir=None, extra_test_file=None, loglevel=logging.DEBUG):
        super(TestGarakPlugin, self).setUp(extra_plugin_dir=self.extra_plugin_dir, extra_test_file=extra_test_file,
                                           loglevel=loglevel)

    def test_plugin_has_methods(self):
        self.assertCommandFound('! hello')
        self.assertCommandFound('! number_44')
        self.assertCommandFound('! spock')
        self.assertCommandFound('! tellme_something')

    def test_mycommand_hello_returns_expected_output(self):
        push_message('! hello')
        self.assertEqual("Hello. You're a killer, admit it. We both are.However, I'm also a very *good* tailor.",
                         pop_message())

    def test_mycommand_number44_returns_expected_output(self):
        push_message('! number 44')
        self.assertEqual("WHOOOO! 44 THAT'S ME!! GETTING SOME COLD CUTS TODAY!!", pop_message())

    def test_mycommand_spock_returns_expected_output(self):
        push_message('! spock')
        self.assertEqual("Live Long and Prosper. - R.I.P Mr. Spock", pop_message())

    def test_mycommand_tellme_something_returns_expected_output(self):
        p = get_plugin_obj_by_name('GarakBot')
        fp = StringIO(json.dumps(self.random_quotes))
        p.garak_quote_ds = fp
        p.clear_garak_quote_datasource()
        push_message('! tellme something')
        self.assertRegex(pop_message(), r'^\w+ Quote!')

    def test_mycommand_tellme_something_with_nodata_fails_gracefully(self):
        p = get_plugin_obj_by_name('GarakBot')
        p.garak_quote_ds = None
        p.clear_garak_quote_datasource()
        self.assertCommand('! tellme something', "I'm Sorry, I have nothing to say. For now.")

    def test_mycommand_tellme_something_returns_random_output(self):
        p = get_plugin_obj_by_name('GarakBot')
        fp = StringIO(json.dumps(self.random_quotes2))
        p.garak_quote_ds = fp
        p.clear_garak_quote_datasource()
        push_message('! tellme something')
        a = pop_message()
        push_message('! tellme something')
        b = pop_message()
        push_message('! tellme something')
        c = pop_message()

        assert a is not None
        assert b is not None
        assert c is not None
        assert a != b != c

    def test_load_data_sources_loads_StringIO_correctly(self):
        p = get_plugin_obj_by_name('GarakBot')
        fp = StringIO(json.dumps(self.random_quotes))
        p.garak_quote_ds = fp
        quote_data = p.load_data_sources()
        assert quote_data is not None
        assert len(quote_data) == len(self.random_quotes)

    def test_load_data_sources_fails_gracefully_with_StringIO(self):
        p = get_plugin_obj_by_name('GarakBot')
        fp = StringIO('')
        p.garak_quote_ds = fp
        quote_data = p.load_data_sources()
        assert quote_data is None

    #Functional TEST
    def test_load_data_sources_loads_DiskFile_correctly(self):
        p = get_plugin_obj_by_name('GarakBot')
        file = NamedTemporaryFile(dir=tempdir, suffix='.json')
        json.dump(self.random_quotes2, open(file.name, mode='w'))
        p.garak_quote_ds = file.name
        quote_data = p.load_data_sources()
        assert quote_data is not None
        assert len(quote_data) == len(self.random_quotes2)


    def test_load_data_sources_fails_gracefully_with_DiskFile(self):
        p = get_plugin_obj_by_name('GarakBot')
        p.garak_quote_ds = 'BAD_FILE'
        quote_data = p.load_data_sources()
        assert quote_data is None

    def test_get_garak_quote_datasource_returns_none_on_empty_file(self):
        p = get_plugin_obj_by_name('GarakBot')
        p.garak_quote_ds = None
        p.clear_garak_quote_datasource()
        quote_data = p.get_garak_quote_datasource()
        assert quote_data is None

    def test_get_garak_quote_datasource_returns_dict(self):
        p = get_plugin_obj_by_name('GarakBot')
        fp = StringIO(json.dumps(self.random_quotes))
        p.garak_quote_ds = fp
        p.clear_garak_quote_datasource()
        quote_data = p.get_garak_quote_datasource()
        assert quote_data is not None
        assert len(quote_data) == 5
        assert self.random_quotes == quote_data
