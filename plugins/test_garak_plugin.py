import os
import sys
import unittest

#sys.path.append(os.pardir+os.sep+"data")
#import config

from errbot.backends.test import testbot, push_message, pop_message
from errbot.plugin_manager import get_plugin_obj_by_name


class TestGarakPlugin(object):
    extra_plugin_dir = '.'

    def test_plugin_methods(self, testbot):
        p = get_plugin_obj_by_name('GarakBot')
        assert p is not None

        assert hasattr(p, 'hello')
        assert hasattr(p, 'get44')



