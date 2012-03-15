.. _glossary:

Glossary
========

.. glossary::
   :sorted:

  Chameleon
    Chameleon is an open-source template engine written in Python_.

  context
    A resource in the resource tree that is found during `traversal
    <http://readthedocs.org/docs/pyramid/en/latest/glossary.html#term-
    traversal>`_ or `URL dispatch
    <http://readthedocs.org/docs/pyramid/en/latest/narr/urldispatch.html>`_
    based on URL data; if it's found via traversal, it's usually a `resource
    <http://readthedocs.org/docs/pyramid/en/latest/glossary.html#term-
    resource>`_ object that is part of a resource tree; if it's found via `URL
    dispatch`_, it's an object manufactured on behalf of the route's "factory".
    A context resource becomes the subject of a :term:`view`, and often has
    security information attached to it.  See the `Traversal Chapter
    <http://readthedocs.org/docs/pyramid/en/latest/narr/traversal.html>`_
    chapter and the `URL dispatch`_ chapter for more information about how a URL
    is resolved to a context resource. See `context in the Pyramid docs
    <http://readthedocs.org/docs/pyramid/en/latest/glossary.html#term-
    context>`_.

  Pyramid
    An awesome `web framework <http://readthedocs.org/docs/pyramid/en/latest/>`_
    that happens to be less opinionated that the author of this entry.

  pyramid_chameleon
    A set of bindings that make templates written for the :term:`Chameleon`
    templating system work under the :term:`Pyramid` web framework.

  renderer
    A serializer that can be referred to via :term:`view configuration` which
    converts a non-:term:`Response` return values from a :term:`view` into a
    string (and ultimately a response).  Using a renderer can make writing views
    that require templating or other serialization less tedious.  See `Views
    which Use a Renderer
    <http://readthedocs.org/docs/pyramid/en/latest/narr/renderers.html#adding-
    and-changing-renderers>`_ for more information.

  renderer factory
    A factory which creates a :term:`renderer`.  See `Adding and Changing
    Renderers <http://readthedocs.org/docs/pyramid/en/latest/narr/renderers.html
    #adding-and-changing-renderers>`_ for more information.

  request
    An object that represents an HTTP request, usually an instance of the
    `pyramid.request.Request <http://readthedocs.org/docs/pyramid/en/latest/api/
    request.html#pyramid.request.Request>`_ class.  See `Webob Chapter
    <http://readthedocs.org/docs/pyramid/en/latest/narr/webob.html#request>`_
    (narrative) and `Request Module
    <http://readthedocs.org/docs/pyramid/en/latest/api/request.html#module-
    pyramid.request>`_ (API documentation) for information about request
    objects.

  response
    An object returned by a :term:`view callable` that represents response data
    returned to the requesting user agent.  It must implements the
    `pyramid.interfaces.IResponse <http://readthedocs.org/docs/pyramid/en/latest/
    api/interfaces.html#pyramid.interfaces.IResponse>`_ interface.  A response
    object is typically an instance of the `pyramid.response.Response
    <http://readthedocs.org/docs/pyramid/en/latest/narr/webob.html#response>`_
    class or a subclass such as `pyramid.httpexceptions.HTTPFound <http://readthe
    docs.org/docs/pyramid/en/latest/api/httpexceptions.html#pyramid.httpexception
    s.HTTPNotFound>`_.  See `Webob Chapter
    <http://readthedocs.org/docs/pyramid/en/latest/narr/webob.html#response>`_
    for information about response objects.

  scan

    The term used by :app:`Pyramid` to define the process of importing and
    examining all code in a Python package or module for `configuration
    decoration <http://readthedocs.org/docs/pyramid/en/latest/glossary.html
    #term-configuration-decoration>`_. See `declarative configuration
    <http://readthedocs.org/docs/pyramid/en/latest/narr/configuration.html
    #declarative-configuration>`_

  template
    A file with replaceable parts that is capable of representing some text,
    XML, or HTML when rendered. See `template in the Pyramid docs
    <http://readthedocs.org/docs/pyramid/en/latest/glossary.html#term-template>`_.

  view
    Common vernacular for a :term:`view callable`.

  view callable
    A "view callable" is a callable Python object which is associated with a
    :term:`view configuration`; it returns a :term:`response` object .  A view
    callable accepts a single argument: ``request``, which will be an instance
    of a :term:`request` object.  An alternate calling convention allows a view
    to be defined as a callable which accepts a pair of arguments: ``context``
    and ``request``: this calling convention is useful for traversal-based
    applications in which a :term:`context` is always very important.  A view
    callable is the primary mechanism by which a developer writes user interface
    code within :app:`Pyramid`.  See `Views Chapter
    <http://readthedocs.org/docs/pyramid/en/latest/narr/views.html>`_ for more
    information about :app:`Pyramid` view callables. See `view callable in the
    Pyramid docs <http://readthedocs.org/docs/pyramid/en/latest/glossary.html
    #term-view- callable>`_.

  view configuration
    View configuration is the act of associating a :term:`view callable` with
    configuration information.  This configuration information helps map a given
    :term:`request` to a particular view callable and it can influence the
    response of a view callable.  :app:`Pyramid` views can be configured via
    `imperative configuration
    <http://readthedocs.org/docs/pyramid/en/latest/glossary.html#term-
    imperative-configuration>`_, or by a special ``@view_config`` decorator
    coupled with a :term:`scan`.  See `View Configuration Chapter
    <http://readthedocs.org/docs/pyramid/en/latest/narr/viewconfig.html>`_ for
    more information about view configuration.

  Zope
    `The Z Object Publishing Framework <http://zope.org>`_, a
    full-featured Python web framework.

  ZPT
    The `Zope Page Template <http://wiki.zope.org/ZPT/FrontPage>`_
    templating language.


.. _Python: http://python.org
