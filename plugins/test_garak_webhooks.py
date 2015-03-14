import os
import sys
import logging
from time import sleep
import socket

import requests
from errbot.backends.test import push_message, pop_message, FullStackTest


config_module = sys.modules['errbot.config-template']
from tempfile import mkdtemp

tempdir = mkdtemp(prefix='/tmp/')
config_module.BOT_DATA_DIR = tempdir
config_module.BOT_LOG_FILE = tempdir + os.sep + 'log.txt'
config_module.BOT_EXTRA_PLUGIN_DIR = []
config_module.BOT_LOG_LEVEL = logging.DEBUG
config_module.GARAK_QUOTE_DATA = '.'
sys.modules['config'] = config_module

# Webserver port is picked based on the process ID so that when tests
# are run in parallel with pytest-xdist, each process runs the server
# on a different port
WEBSERVER_PORT = 5000 + (os.getpid() % 1000)
WEBSERVER_SSL_PORT = WEBSERVER_PORT + 1000

EXTRA_PLUGIN_DIR = "."


def webserver_ready(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        return True
    except:
        return False


class TestGarakPluginWebHooks(FullStackTest):
    def setUp(self, extra_plugin_dir=None, extra_test_file=None, loglevel=logging.DEBUG):
        super(TestGarakPluginWebHooks, self).setUp(extra_plugin_dir=EXTRA_PLUGIN_DIR, extra_test_file=extra_test_file,
                                                   loglevel=loglevel)
        push_message("!config Webserver {{'HOST': 'localhost', 'PORT': {}, 'SSL':  None}}".format(WEBSERVER_PORT))
        pop_message()
        while not webserver_ready('localhost', WEBSERVER_PORT):
            logging.debug("Webserver not ready yet, sleeping 0.1 second")
            sleep(0.1)

    def test_webserver_plugin_ok(self):
        push_message("!webstatus")
        response = pop_message()
        print(response)
        assert "/echo/" in response

    def test_not_configured_url_returns_404(self):
        assert requests.post(
            'http://localhost:{}/randomness_blah'.format(WEBSERVER_PORT),
            "{'toto': 'titui'}"
        ).status_code == 404

    def test_webhook_spock_returns_expected_string(self):
        response = requests.post(
            'http://localhost:{}/spock/'.format(WEBSERVER_PORT),
            data=None
        ).text
        print(response)
        self.assertEquals(response, "Live Long and Prosper. - R.I.P Mr. Spock")

