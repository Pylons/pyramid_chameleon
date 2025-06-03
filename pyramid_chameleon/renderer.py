import os
import re
import threading

try:
    # we need to try the backport first, as we rely on ``files`` added in 3.9
    import importlib_resources
except ImportError:
    import importlib.resources as importlib_resources

from zope.interface import implementer

from pyramid.asset import (
    asset_spec_from_abspath,
    resolve_asset_spec,
    )

from pyramid.path import (
    caller_package,
    package_path
    )

from pyramid_chameleon.interfaces import (
    IChameleonLookup,
    IChameleonTranslate,
    ITemplateRenderer,
    )


@implementer(IChameleonLookup)
class ChameleonRendererLookup(object):
    spec_re = re.compile(
        r'(?P<asset>[\w_.:/-]+)'
        r'(?:\#(?P<defname>[\w_]+))?'
        r'(\.(?P<ext>.*))'
        )

    def __init__(self, impl, registry):
        self.impl = impl
        self.registry = registry
        self.lock = threading.Lock()

    def get_spec(self, name, package):
        (package, name) = resolve_asset_spec(name, package)

        if not package:
            # if there's no package, we can't do any conversion
            return name

        return "%s:%s" % (package, name)

    @property # wait until completely necessary to look up translator
    def translate(self):
        return self.registry.queryUtility(IChameleonTranslate)

    @property # wait until completely necessary to look up debug_templates
    def debug(self):
        settings = self.registry.settings
        if settings is None:
            return False
        return settings.get('debug_templates', False)

    @property # wait until completely necessary to look up reload_templates
    def auto_reload(self):
        settings = self.registry.settings
        if settings is None:
            return False
        return settings.get('reload_templates', False)

    def _crack_spec(self, spec):
        asset, macro, ext = self.spec_re.match(spec).group(
            'asset', 'defname', 'ext'
            )
        return asset, macro, ext

    def __call__(self, info):
        spec = self.get_spec(info.name, info.package)
        registry = info.registry

        if os.path.isabs(spec):
            # 'spec' is an absolute filename
            if not os.path.exists(spec):
                raise ValueError('Missing template file: %s' % spec)
            renderer = registry.queryUtility(ITemplateRenderer, name=spec)
            if renderer is None:
                renderer = self.impl(spec, self, macro=None)
                # cache the template
                with self.lock:
                    registry.registerUtility(renderer,
                                             ITemplateRenderer, name=spec)
        else:
            # spec is a package:relpath asset spec
            renderer = registry.queryUtility(ITemplateRenderer, name=spec)
            if renderer is None:
                asset, macro, ext = self._crack_spec(spec)
                spec_without_macro = '%s.%s' % (asset, ext)
                try:
                    package_name, filename = spec_without_macro.split(':', 1)
                except ValueError: # pragma: no cover
                    # somehow we were passed a relative pathname; this
                    # should die
                    package_name = caller_package(4).__name__
                    filename = spec_without_macro
                files = importlib_resources.files(package_name)
                if not files.joinpath(filename).exists():
                    raise ValueError(
                        'Missing template asset: %s (%s)' % (
                            spec_without_macro, filename)
                        )
                renderer = self.impl(spec, self, macro=macro)
                settings = info.settings
                if not settings.get('reload_assets'):
                    # cache the template
                    with self.lock:
                        registry.registerUtility(renderer, ITemplateRenderer,
                                                 name=spec)

        return renderer

registry_lock = threading.Lock()

def template_renderer_factory(info, impl, lock=registry_lock):
    registry = info.registry
    lookup = registry.queryUtility(IChameleonLookup, name=info.type)
    if lookup is None:
        lookup = ChameleonRendererLookup(impl, registry)
        with lock:
            registry.registerUtility(lookup, IChameleonLookup, name=info.type)
    return lookup(info)

