import os
import threading

import pkg_resources

from translationstring import ChameleonTranslate

from zope.interface import implementer

from pyramid.asset import asset_spec_from_abspath
from pyramid.interfaces import ITemplateRenderer
from pyramid.config.i18n import translator
from pyramid.path import (
    caller_package,
    package_path
    )

from pyramid_chameleon import (
    chameleon_text,
    chameleon_zpt
    )

from pyramid_chameleon.interfaces import (
    IChameleonLookup,
    IChameleonTranslate
    )

RENDERERS = (
    ('.txt', chameleon_text.renderer_factory),
    ('.pt', chameleon_zpt.renderer_factory)
    )


@implementer(IChameleonLookup)
class ChameleonRendererLookup(object):
    def __init__(self, impl, registry):
        self.impl = impl
        self.registry = registry
        self.lock = threading.Lock()

    def get_spec(self, name, package):
        if not package:
            # if there's no package, we can't do any conversion
            return name

        spec = name
        isabspath = os.path.isabs(name)
        colon_in_name = ':' in name
        isabsspec = colon_in_name and (not isabspath)
        isrelspec = (not isabsspec) and (not isabspath)

        # if it's already an absolute spec, we don't need to do anything,
        # but if it's a relative spec or an absolute path, we need to try
        # to convert it to an absolute spec

        if isrelspec:
            # convert relative asset spec to absolute asset spec
            pp = package_path(package)
            spec = os.path.join(pp, spec)
            spec = asset_spec_from_abspath(spec, package)

        elif isabspath:
            # convert absolute path to absolute asset spec
            spec = asset_spec_from_abspath(spec, package)

        return spec

    @property  # wait until completely necessary to look up translator
    def translate(self):
        return self.registry.queryUtility(IChameleonTranslate)

    @property  # wait until completely necessary to look up debug_templates
    def debug(self):
        settings = self.registry.settings
        if settings is None:
            return False
        return settings.get('debug_templates', False)

    @property  # wait until completely necessary to look up reload_templates
    def auto_reload(self):
        settings = self.registry.settings
        if settings is None:
            return False
        return settings.get('reload_templates', False)

    def __call__(self, info):
        spec = self.get_spec(info.name, info.package)
        registry = info.registry

        if os.path.isabs(spec):
            # 'spec' is an absolute filename
            if not os.path.exists(spec):
                raise ValueError('Missing template file: %s' % spec)
            renderer = registry.queryUtility(ITemplateRenderer, name=spec)
            if renderer is None:
                renderer = self.impl(spec, self)
                # cache the template
                try:
                    self.lock.acquire()
                    registry.registerUtility(renderer,
                                             ITemplateRenderer, name=spec)
                finally:
                    self.lock.release()
        else:
            # spec is a package:relpath asset spec
            renderer = registry.queryUtility(ITemplateRenderer, name=spec)
            if renderer is None:
                try:
                    package_name, filename = spec.split(':', 1)
                except ValueError:  # pragma: no cover
                    # somehow we were passed a relative pathname; this
                    # should die
                    package_name = caller_package(4).__name__
                    filename = spec
                abspath = pkg_resources.resource_filename(package_name,
                                                          filename)
                if not pkg_resources.resource_exists(package_name, filename):
                    raise ValueError(
                        'Missing template asset: %s (%s)' % (spec, abspath))
                renderer = self.impl(abspath, self)
                settings = info.settings
                if not settings.get('reload_assets'):
                    # cache the template
                    self.lock.acquire()
                    try:
                        registry.registerUtility(renderer, ITemplateRenderer,
                                                 name=spec)
                    finally:
                        self.lock.release()

        return renderer


registry_lock = threading.Lock()


def template_renderer_factory(info, impl, lock=registry_lock):
    registry = info.registry
    lookup = registry.queryUtility(IChameleonLookup, name=info.type)
    if lookup is None:
        lookup = ChameleonRendererLookup(impl, registry)
        lock.acquire()
        try:
            registry.registerUtility(lookup, IChameleonLookup, name=info.type)
        finally:
            lock.release()
    return lookup(info)


def includeme(config):
    config.add_renderer('.pt', chameleon_zpt.renderer_factory)
    config.add_renderer('.txt', chameleon_text.renderer_factory)
    ctranslate = ChameleonTranslate(translator)
    config.registry.registerUtility(ctranslate, IChameleonTranslate)
