import unittest
import tempfile
import os
import shutil

class Test__compile_one(unittest.TestCase):
    def setUp(self):
        import chameleon.config
        self._cache_dir = tempfile.mkdtemp()
        self._old_cache_dir = chameleon.config.CACHE_DIRECTORY
        chameleon.config.CACHE_DIRECTORY = self._cache_dir

    def tearDown(self):
        import chameleon.config
        chameleon.config.CACHE_DIRECTORY = self._old_cache_dir
        shutil.rmtree(self._cache_dir)

    def _getTemplateDir(self):
        here = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(here, 'fixtures')

    def _callFUT(self, args):
        from pyramid_chameleon.precompile import _compile_one
        return _compile_one(args)

    def test_keyboard_interrupt(self):
        try:
            import pyramid_chameleon.precompile
            _old = pyramid_chameleon.precompile.compile_one
            def compile_one_raise(fullpath, template_factory):
                self.assertEqual(fullpath, None)
                self.assertEqual(template_factory, None)
                raise KeyboardInterrupt()
            pyramid_chameleon.precompile.compile_one = compile_one_raise
            result = self._callFUT((None, None, None))
            self.assertEqual(result, {'path':None, 'success':False})
        finally:
            pyramid_chameleon.precompile.compile_one = _old

    def test_other_exception_fail_fast(self):
        try:
            import pyramid_chameleon.precompile
            _old = pyramid_chameleon.precompile.compile_one
            def compile_one_raise(fullpath, template_factory):
                self.assertEqual(fullpath, None)
                self.assertEqual(template_factory, None)
                raise ValueError()
            pyramid_chameleon.precompile.compile_one = compile_one_raise
            self.assertRaises(ValueError, self._callFUT, (None, None, True))
        finally:
            pyramid_chameleon.precompile.compile_one = _old

    def test_other_exception_no_fail_fast(self):
        try:
            import pyramid_chameleon.precompile
            _old = pyramid_chameleon.precompile.compile_one
            def compile_one_raise(fullpath, template_factory):
                self.assertEqual(fullpath, None)
                self.assertEqual(template_factory, None)
                raise ValueError()
            pyramid_chameleon.precompile.compile_one = compile_one_raise
            result = self._callFUT((None, None, False))
            self.assertEqual(result, {'path':None, 'success':False})
        finally:
            pyramid_chameleon.precompile.compile_one = _old

    def test_gardenpath(self):
        templatedir = self._getTemplateDir()
        templatepath = os.path.join(templatedir, 'minimal.pt')
        class DummyTemplateFactory(object):
            def __call__(innerself, fullpath, macro=None):
                self.assertEqual(fullpath, templatepath)
                return innerself
            def cook_check(innerself):
                innerself.checked = True
        factory = DummyTemplateFactory()
        result = self._callFUT((templatepath, factory, False))
        self.assertEqual(result, {'path':templatepath, 'success':True})
        self.assertTrue(factory.checked)

class Test_functional(unittest.TestCase):

    def setUp(self):
        import chameleon.config
        self._cache_dir = tempfile.mkdtemp()
        self._old_cache_dir = chameleon.config.CACHE_DIRECTORY
        chameleon.config.CACHE_DIRECTORY = self._cache_dir

    def tearDown(self):
        import chameleon.config
        chameleon.config.CACHE_DIRECTORY = self._old_cache_dir
        shutil.rmtree(self._cache_dir)

    def _getTemplateDir(self):
        here = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(here, 'fixtures')

    def test_no_cache_dir(self):
        import chameleon.config
        try:
            _old = chameleon.config.CACHE_DIRECTORY
            chameleon.config.CACHE_DIRECTORY = None
            from pyramid_chameleon.precompile import precompile
            result = precompile(argv=['bin', '--dir', self._getTemplateDir()])
            self.assertEqual(result, 1)
        finally:
            chameleon.config.CACHE_DIRECTORY = _old

    def test_posargs(self):
        from pyramid_chameleon.precompile import precompile
        result = precompile(
            argv=['bin', 'posarg', '--dir', self._getTemplateDir()]
        )
        self.assertEqual(result, 1)

    def test_notemplates(self):
        try:
            templatedir = tempfile.mkdtemp()
            from pyramid_chameleon.precompile import precompile
            result = precompile(argv=['bin', '--dir', templatedir])
        finally:
            shutil.rmtree(templatedir)
        self.assertEqual(result, 1)

    def test_works(self):
        from pyramid_chameleon.precompile import precompile
        result = precompile(argv=['bin', '--dir', self._getTemplateDir()])
        self.assertEqual(result, 0)
