import unittest
import tempfile
import os
import shutil

class Test_functional(unittest.TestCase):

    def setUp(self):
        import chameleon.config
        self._cache_dir = tempfile.mkdtemp()
        self._old_cache_dir = chameleon.config.CACHE_DIRECTORY
        chameleon.config.CACHE_DIRECTORY = self._cache_dir

    def _getTemplateDir(self):
        import os
        here = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(here, 'fixtures')

    def test_works(self):
        from pyramid_chameleon.precompile import precompile
        result = precompile(argv=['bin', '--dir', self._getTemplateDir()])
        self.assertEquals(result, 0)

    def tearDown(self):
        import chameleon.config
        chameleon.config.CACHE_DIRECTORY = self._old_cache_dir
        shutil.rmtree(self._cache_dir)
