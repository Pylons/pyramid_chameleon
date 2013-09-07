import unittest
from pyramid import testing

class Test_maybe_add_translator(unittest.TestCase):
    def _callFUT(self, registry):
        from ..localization import maybe_add_translator
        return maybe_add_translator(registry)
    
    def test_translation_dirs_exist(self):
        registry = DummyRegistry(None)
        self._callFUT(registry)
        self.assertEqual(registry.registered, None)

    def test_no_translation_dirs(self):
        registry = DummyRegistry(True)
        self._callFUT(registry)
        self.assertTrue(registry.registered)

class Test_translator(unittest.TestCase):
    def setUp(self):
        from pyramid.request import Request
        request = Request.blank('/')
        self.config = testing.setUp(request=request)
        request.registry = self.config.registry

    def tearDown(self):
        testing.tearDown()
        
    def _callFUT(self, msg):
        from ..localization import translator
        return translator(msg)

    def test_it(self):
        result = self._callFUT('foo')
        self.assertEqual(result, 'foo')
    
class DummyRegistry(object):
    registered = None
    def __init__(self, result):
        self.result = result
        
    def queryUtility(self, iface):
        return self.result

    def registerUtility(self, impl, iface):
        self.registered = (impl, iface)
