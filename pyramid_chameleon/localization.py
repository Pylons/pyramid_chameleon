from translationstring import ChameleonTranslate
from pyramid.interfaces import ITranslationDirectories
from pyramid.threadlocal import get_current_request
from pyramid.i18n import get_localizer

from .interfaces import IChameleonTranslate

def translator(msg):
    request = get_current_request()
    localizer = get_localizer(request)
    return localizer.translate(msg)

def maybe_add_translator(registry):
    # only conditionally register a translator if there are actually
    # translation directories (for performance reasons)
    if registry.queryUtility(ITranslationDirectories) is not None:
        ctranslate = ChameleonTranslate(translator)
        registry.registerUtility(ctranslate, IChameleonTranslate)

def includeme(config): # pragma: no cover
    """
    Adds renderers for .pt and .txt as well as registers a Chameleon
    translation utility
    """
    # use order=1000 to take effect very late (in particular, after
    # any effect that config.add_translation_dirs has)
    config.action(None, callable=maybe_add_translator, args=(config.registry,),
                  order=1000)
