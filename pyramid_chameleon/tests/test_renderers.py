import unittest

from pyramid.testing import cleanUp
from pyramid import testing

class TestTemplateRendererFactory(unittest.TestCase):
    def setUp(self):
        self.config = cleanUp()

    def tearDown(self):
        cleanUp()

    def _callFUT(self, info, impl):
        from pyramid_chameleon.renderer import template_renderer_factory
        return template_renderer_factory(info, impl)

    def test_lookup_found(self):
        from pyramid_chameleon.interfaces import IChameleonLookup
        L = []

        def dummy(info):
            L.append(info)
            return True
        self.config.registry.registerUtility(dummy, IChameleonLookup,
                                             name='abc')

        class DummyInfo(object):
            pass
        info = DummyInfo()
        info.registry = self.config.registry
        info.type = 'abc'
        result = self._callFUT(info, None)
        self.assertEqual(result, True)
        self.assertEqual(L, [info])

    def test_lookup_miss(self):
        from pyramid_chameleon.interfaces import ITemplateRenderer
        import os
        abspath = os.path.abspath(__file__)
        renderer = {}
        self.config.registry.registerUtility(
            renderer, ITemplateRenderer, name=abspath)
        info = DummyRendererInfo({
            'name': abspath,
            'package': None,
            'registry': self.config.registry,
            'settings': {},
            'type': 'type',
            })
        result = self._callFUT(info, None)
        self.assertTrue(result is renderer)


class TestChameleonRendererLookup(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def _makeOne(self, impl):
        from pyramid_chameleon.renderer import ChameleonRendererLookup
        return ChameleonRendererLookup(impl, self.config.registry)

    def _registerTemplateRenderer(self, renderer, name):
        from pyramid_chameleon.interfaces import ITemplateRenderer
        self.config.registry.registerUtility(
            renderer, ITemplateRenderer, name=name)

    def test_get_spec_not_abspath_no_colon_no_package(self):
        lookup = self._makeOne(None)
        result = lookup.get_spec('foo', None)
        self.assertEqual(result, 'foo')

    def test_get_spec_not_abspath_no_colon_with_package(self):
        from pyramid_chameleon import tests
        lookup = self._makeOne(None)
        result = lookup.get_spec('foo', tests)
        self.assertEqual(result, 'pyramid_chameleon.tests:foo')

    def test_get_spec_not_abspath_with_colon_no_package(self):
        lookup = self._makeOne(None)
        result = lookup.get_spec('fudge:foo', None)
        self.assertEqual(result, 'fudge:foo')

    def test_get_spec_not_abspath_with_colon_with_package(self):
        from pyramid_chameleon import tests
        lookup = self._makeOne(None)
        result = lookup.get_spec('fudge:foo', tests)
        self.assertEqual(result, 'fudge:foo')

    def test_get_spec_is_abspath_no_colon_no_package(self):
        import os
        lookup = self._makeOne(None)
        spec = os.path.abspath(__file__)
        result = lookup.get_spec(spec, None)
        self.assertEqual(result, spec)

    def test_get_spec_is_abspath_no_colon_with_path_in_package(self):
        from pyramid_chameleon import tests
        import os
        lookup = self._makeOne(None)
        f = __file__
        spec = os.path.abspath(f)
        result = lookup.get_spec(spec, tests)
        self.assertEqual(result, 'pyramid_chameleon.tests:%s' % os.path.split(f)[-1])

    def test_get_spec_is_abspath_no_colon_with_path_outside_package(self):
        # venusian used only because it's outside of pyramid_chameleon.tests
        import venusian 
        import os
        lookup = self._makeOne(None)
        f = __file__
        spec = os.path.abspath(f)
        result = lookup.get_spec(spec, venusian)
        self.assertEqual(result, spec)

    def test_get_spec_is_abspath_with_colon_no_package(self):
        import os
        lookup = self._makeOne(None)
        spec = os.path.join(os.path.abspath(__file__), ':foo')
        result = lookup.get_spec(spec, None)
        self.assertEqual(result, spec)

    def test_get_spec_is_abspath_with_colon_with_path_in_package(self):
        from pyramid_chameleon import tests
        import os
        lookup = self._makeOne(None)
        f = os.path.abspath(__file__)
        spec = os.path.join(f, ':foo')
        result = lookup.get_spec(spec, tests)
        tail = spec.split(os.sep)[-2:]
        self.assertEqual(result, 'pyramid_chameleon.tests:%s/%s' % tuple(tail))

    def test_get_spec_is_abspath_with_colon_with_path_outside_package(self):
        # venusian used only because it's outside of pyramid_chameleon.tests
        import venusian
        import os
        lookup = self._makeOne(None)
        spec = os.path.join(os.path.abspath(__file__), ':foo')
        result = lookup.get_spec(spec, venusian)
        self.assertEqual(result, spec)

    def test_translate(self):
        from pyramid_chameleon.interfaces import IChameleonTranslate
        def t(): pass
        self.config.registry.registerUtility(t, IChameleonTranslate)
        lookup = self._makeOne(None)
        self.assertEqual(lookup.translate, t)

    def test_debug_settings_None(self):
        self.config.registry.settings = None
        lookup = self._makeOne(None)
        self.assertEqual(lookup.debug, False)

    def test_debug_settings_not_None(self):
        self.config.registry.settings = {'debug_templates':True}
        lookup = self._makeOne(None)
        self.assertEqual(lookup.debug, True)

    def test_auto_reload_settings_None(self):
        self.config.registry.settings = None
        lookup = self._makeOne(None)
        self.assertEqual(lookup.auto_reload, False)

    def test_auto_reload_settings_not_None(self):
        self.config.registry.settings = {'reload_templates':True}
        lookup = self._makeOne(None)
        self.assertEqual(lookup.auto_reload, True)

    def test___call__abspath_path_notexists(self):
        abspath = '/wont/exist'
        self._registerTemplateRenderer({}, abspath)
        info = DummyRendererInfo({
            'name':abspath,
            'package':None,
            'registry':self.config.registry,
            'settings':{},
            'type':'type',
            })
        lookup = self._makeOne(None)
        self.assertRaises(ValueError, lookup.__call__, info)

    def test___call__abspath_alreadyregistered(self):
        import os
        abspath = os.path.abspath(__file__)
        renderer = {}
        self._registerTemplateRenderer(renderer, abspath)
        info = DummyRendererInfo({
            'name':abspath,
            'package':None,
            'registry':self.config.registry,
            'settings':{},
            'type':'type',
            })
        lookup = self._makeOne(None)
        result = lookup(info)
        self.assertTrue(result is renderer)

    def test___call__abspath_notyetregistered(self):
        import os
        abspath = os.path.abspath(__file__)
        renderer = {}
        factory = DummyFactory(renderer)
        info = DummyRendererInfo({
            'name':abspath,
            'package':None,
            'registry':self.config.registry,
            'settings':{},
            'type':'type',
            })
        lookup = self._makeOne(factory)
        result = lookup(info)
        self.assertEqual(result, renderer)

    def test___call__relpath_path_registered(self):
        renderer = {}
        spec = 'foo/bar'
        self._registerTemplateRenderer(renderer, spec)
        info = DummyRendererInfo({
            'name':spec,
            'package':None,
            'registry':self.config.registry,
            'settings':{},
            'type':'type',
            })
        lookup = self._makeOne(None)
        result = lookup(info)
        self.assertTrue(renderer is result)

    def test___call__relpath_has_package_registered(self):
        renderer = {}
        import pyramid_chameleon.tests
        spec = 'bar/baz'
        self._registerTemplateRenderer(
            renderer, 'pyramid_chameleon.tests:bar/baz')
        info = DummyRendererInfo({
            'name':spec,
            'package':pyramid_chameleon.tests,
            'registry':self.config.registry,
            'settings':{},
            'type':'type',
            })
        lookup = self._makeOne(None)
        result = lookup(info)
        self.assertTrue(renderer is result)

    def test___call__spec_notfound(self):
        spec = 'pyramid_chameleon.tests:wont/exist'
        info = DummyRendererInfo({
            'name':spec,
            'package':None,
            'registry':self.config.registry,
            'settings':{},
            'type':'type',
            })
        lookup = self._makeOne(None)
        self.assertRaises(ValueError, lookup.__call__, info)

    def test___call__spec_alreadyregistered(self):
        from pyramid import tests
        module_name = tests.__name__
        relpath = 'test_renderers.py'
        spec = '%s:%s' % (module_name, relpath)
        info = DummyRendererInfo({
            'name':spec,
            'package':None,
            'registry':self.config.registry,
            'settings':{},
            'type':'type',
            })
        renderer = {}
        self._registerTemplateRenderer(renderer, spec)
        lookup = self._makeOne(None)
        result = lookup(info)
        self.assertTrue(result is renderer)

    def test___call__spec_notyetregistered(self):
        import os
        from pyramid_chameleon import tests
        module_name = tests.__name__
        relpath = 'test_renderers.py'
        renderer = {}
        factory = DummyFactory(renderer)
        spec = '%s:%s' % (module_name, relpath)
        info = DummyRendererInfo({
            'name':spec,
            'package':None,
            'registry':self.config.registry,
            'settings':{},
            'type':'type',
            })
        lookup = self._makeOne(factory)
        result = lookup(info)
        self.assertTrue(result is renderer)
        path = os.path.abspath(__file__).split('$')[0] # jython
        if path.endswith('.pyc'): # pragma: no cover
            path = path[:-1]
        self.assertTrue(factory.path.startswith(path))
        self.assertEqual(factory.kw, {'macro':None})

    def test___call__spec_withmacro(self):
        from pyramid_chameleon.interfaces import ITemplateRenderer
        import os
        from pyramid_chameleon import tests
        module_name = tests.__name__
        relpath = 'fixtures/withmacro#foo.pt'
        renderer = {}
        factory = DummyFactory(renderer)
        spec = '%s:%s' % (module_name, relpath)
        reg = self.config.registry
        info = DummyRendererInfo({
            'name':spec,
            'package':None,
            'registry':reg,
            'settings':{},
            'type':'type',
            })
        lookup = self._makeOne(factory)
        result = lookup(info)
        self.assertTrue(result is renderer)
        path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'fixtures',
            'withmacro.pt')
        self.assertTrue(factory.path.startswith(path))
        self.assertEqual(factory.kw, {'macro':'foo'})
        self.assertTrue(
            reg.getUtility(ITemplateRenderer, name=spec) is renderer
            )

    def test___call__reload_assets_true(self):
        import pyramid_chameleon.tests
        from pyramid.interfaces import ISettings
        from pyramid_chameleon.interfaces import ITemplateRenderer
        settings = {'reload_assets':True}
        self.config.registry.registerUtility(settings, ISettings)
        renderer = {}
        factory = DummyFactory(renderer)
        spec = 'test_renderers.py'
        reg = self.config.registry
        info = DummyRendererInfo({
            'name':spec,
            'package':pyramid_chameleon.tests,
            'registry':reg,
            'settings':settings,
            'type':'type',
            })
        lookup = self._makeOne(factory)
        result = lookup(info)
        self.assertTrue(result is renderer)
        spec = '%s:%s' % ('pyramid_chameleon.tests', 'test_renderers.py')
        self.assertEqual(reg.queryUtility(ITemplateRenderer, name=spec),
                         None)

    def test___call__reload_assets_false(self):
        import pyramid_chameleon.tests
        from pyramid_chameleon.interfaces import ITemplateRenderer
        settings = {'reload_assets':False}
        renderer = {}
        factory = DummyFactory(renderer)
        spec = 'test_renderers.py'
        reg = self.config.registry
        info = DummyRendererInfo({
            'name':spec,
            'package':pyramid_chameleon.tests,
            'registry':reg,
            'settings':settings,
            'type':'type',
            })
        lookup = self._makeOne(factory)
        result = lookup(info)
        self.assertTrue(result is renderer)
        spec = '%s:%s' % ('pyramid_chameleon.tests', 'test_renderers.py')
        self.assertNotEqual(reg.queryUtility(ITemplateRenderer, name=spec),
                            None)


class Dummy:
    pass

class DummyResponse:
    status = '200 OK'
    headerlist = ()
    app_iter = ()
    body = ''

class DummyFactory:
    def __init__(self, renderer):
        self.renderer = renderer

    def __call__(self, path, lookup, **kw):
        self.path = path
        self.kw = kw
        return self.renderer


class DummyRendererInfo(object):
    def __init__(self, kw):
        self.__dict__.update(kw)

