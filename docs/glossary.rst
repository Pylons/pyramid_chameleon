.. _glossary:

Glossary
========

.. glossary::
    :sorted:

    Babel
        A `collection of tools <https://babel.pocoo.org/en/latest/>`_ for internationalizing Python applications.
        :app:`Pyramid` does not depend on Babel to operate, but if Babel is installed, additional locale functionality becomes available to your application.

    Chameleon
        `Chameleon <https://chameleon.readthedocs.io/en/latest/>`_ is an open-source template engine written in `Python <https://www.python.org>`_.

    Genshi
        An `XML templating language <https://pypi.org/project/Genshi/>`_ by Christopher Lenz.

    Mako
        `Mako <https://www.makotemplates.org/>`_ is a template language which refines the familiar ideas of componentized layout and inheritance using Python with Python scoping and calling semantics.

    Response
        An object returned by a view callable that represents response data returned to the requesting user agent.
        It must implement the :class:`pyramid.interfaces.IResponse` interface.
        A response object is typically an instance of the :class:`pyramid.response.Response` class or a subclass such as :class:`pyramid.httpexceptions.HTTPFound`.
        See :ref:`pyramid:webob_chapter` for information about response objects.

    ZPT
        ZPT is the `Zope Page Template <https://zope.readthedocs.io/en/latest/zopebook/ZPT.html>`_ templating language.
