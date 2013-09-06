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
