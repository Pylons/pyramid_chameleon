from translationstring import ChameleonTranslate
from pyramid.config.i18n import translator
from pyramid.interfaces import ITranslationDirectories

from pyramid_chameleon import (
    chameleon_text,
    chameleon_zpt
    )

from pyramid_chameleon.interfaces import IChameleonTranslate

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
    config.add_renderer('.pt', chameleon_zpt.renderer_factory)
    config.add_renderer('.txt', chameleon_text.renderer_factory)
    # use order=1000 to take effect very late (in particular, after
    # any effect that config.add_translation_dirs has)
    config.action(None, callable=maybe_add_translator, args=config.registry,
                  order=1000)
