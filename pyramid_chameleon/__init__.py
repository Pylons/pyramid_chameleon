from . import (
    text,
    zpt,
    )

def includeme(config): # pragma: no cover
    """
    Adds renderers for .pt and .txt as well as registers Chameleon
    localization features.
    """
    config.add_renderer('.pt', zpt.renderer_factory)
    config.add_renderer('.txt', text.renderer_factory)
    config.include('.localization')
