from translationstring import ChameleonTranslate
from pyramid.config.i18n import translator

from pyramid_chameleon import (
    chameleon_text,
    chameleon_zpt
    )

from pyramid_chameleon.interfaces import IChameleonTranslate


def includeme(config):
    config.add_renderer('.pt', chameleon_zpt.renderer_factory)
    config.add_renderer('.txt', chameleon_text.renderer_factory)
    ctranslate = ChameleonTranslate(translator)
    config.registry.registerUtility(ctranslate, IChameleonTranslate)
