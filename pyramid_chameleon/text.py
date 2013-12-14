from zope.interface import implementer

from pyramid_chameleon.interfaces import IChameleonTemplateRenderer

from pyramid.decorator import reify
from pyramid_chameleon import renderer

def renderer_factory(info):
    return renderer.template_renderer_factory(info, TextTemplateRenderer)

@implementer(IChameleonTemplateRenderer)
class TextTemplateRenderer(object):
    def __init__(self, path, lookup, macro=None):
        self.path = path
        self.lookup = lookup
        # text template renderers have no macros, so we ignore the
        # macro arg

    @reify # avoid looking up reload_templates before manager pushed
    def template(self):
        from chameleon.zpt.template import PageTextTemplateFile
        return PageTextTemplateFile(self.path,
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
