from zope.interface import (
    Attribute,
    Interface,
    )


class IChameleonLookup(Interface):
    translate = Attribute('IChameleonTranslate object')
    debug = Attribute('The ``debug_templates`` setting for this application')
    auto_reload = Attribute('The ``reload_templates`` setting for this app')
    def __call__(self, info):
        """ Return an ITemplateRenderer based on IRendererInfo ``info`` """

class IChameleonTranslate(Interface):
    """ Internal interface representing a chameleon translate function """
    def __call__(msgid, domain=None, mapping=None, context=None,
                 target_language=None, default=None):
        """ Translate a mess of arguments to a Unicode object """

from zope.deprecation import __show__
try:
    __show__.off()
    # For backwards compatibility, as long as ITemplateRenderer
    # exists, we will still implement that.
    from pyramid.interfaces import ITemplateRenderer
    class IChameleonTemplateRenderer(ITemplateRenderer):
        "Chameleon-specific template renderer"
except ImportError:
    from pyramid.interfaces import IRenderer
    class IChameleonTemplateRenderer(IRenderer):
        "Chameleon-specific template renderer"
        def implementation():
            """ Return the object that the underlying templating system
            uses to render the template; it is typically a callable that
            accepts arbitrary keyword arguments and returns a string or
            unicode object """
finally:
    __show__.on()
