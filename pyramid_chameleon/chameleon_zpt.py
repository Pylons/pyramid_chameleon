import sys

from zope.deprecation import deprecated
from zope.interface import implementer

from pyramid.compat import reraise

try:
    from chameleon.zpt.template import PageTemplateFile
    PageTemplateFile  # prevent pyflakes complaining about a redefinition below
except ImportError:  # pragma: no cover
    exc_class, exc, tb = sys.exc_info()

    # Chameleon doesn't work on non-CPython platforms
    class PageTemplateFile(object):
        def __init__(self, *arg, **kw):
            reraise(ImportError, exc, tb)

from pyramid.interfaces import ITemplateRenderer

from pyramid.decorator import reify
from pyramid_chameleon.renderer import template_renderer_factory


def renderer_factory(info):
    return template_renderer_factory(info, ZPTTemplateRenderer)


@implementer(ITemplateRenderer)
class ZPTTemplateRenderer(object):
    def __init__(self, path, lookup):
        self.path = path
        self.lookup = lookup

    @reify  # avoid looking up reload_templates before manager pushed
    def template(self):
        if sys.platform.startswith('java'):  # pragma: no cover
            raise RuntimeError(
                'Chameleon templates are not compatible with Jython')
        return PageTemplateFile(self.path,
                                auto_reload=self.lookup.auto_reload,
                                debug=self.lookup.debug,
                                translate=self.lookup.translate)

    def implementation(self):
        return self.template

    def __call__(self, value, system):
        try:
            system.update(value)
        except (TypeError, ValueError):
            raise ValueError('renderer was passed non-dictionary as value')
        result = self.template(**system)
        return result
