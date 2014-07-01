from zope.interface import (
    Attribute,
    Interface,
    )
from pyramid.interfaces import IRenderer

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

class ITemplateRenderer(IRenderer):
    def implementation():
        """ Return the object that the underlying templating system
        uses to render the template; it is typically a callable that
        accepts arbitrary keyword arguments and returns a string or
        unicode object """
