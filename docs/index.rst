=================
pyramid_chameleon
=================

Overview
========

:mod:`pyramid_chameleon` is a set of bindings that make templates written for
the :term:`Chameleon` templating system work under the Pyramid web
framework.

Installation
============

Install using setuptools, e.g. (within a virtualenv)::

  $ $myvenv/bin/easy_install pyramid_chameleon

Setup
=====

There are several ways to make sure that :mod:`pyramid_chameleon` is active.
They are completely equivalent:

#) Add pyramid_chameleon to the `pyramid.includes` section of your applications
   main configuration section::

    [app:main]
    ...
    pyramid.includes = pyramid_chameleon


#) Use the ``includeme`` function via ``config.include``::

    config.include('pyramid_chameleon')

Once activated, files with the ``.pt`` extension are considered to be
:term:`Chameleon` templates.

.. _using_chameleon_templates:

Using Chameleon Templates
=========================

Once :mod:`pyramid_chameleon` been activated ``.pt`` templates can be loaded
either by looking up names that would be found on the :term:`Chameleon` search
path or by looking up an absolute asset specification (see
:ref:`asset_specifications` for more information).

Quick example 1.  Look up a template named ``foo.pt`` within the ``templates``
directory of a Python package named ``mypackage``:

.. code-block:: python
   :linenos:

    @view_config(renderer="mypackage:templates/foo.pt)
    def sample_view(request):
       return {'foo':1, 'bar':2}

Quick example 2.  Look up a template named ``foo.pt`` within the ``templates``
directory of the "current" Python package (the package in which this Python
code is defined):

.. code-block:: python
   :linenos:

    @view_config(renderer="templates/foo.pt)
    def sample_view(request):
       return {'foo':1, 'bar':2}

Quick example 3: manufacturing a response object using the result of
:func:`~pyramid.renderers.render` (a string) using a Chameleon template:

.. code-block:: python
   :linenos:

   from pyramid.renderers import render
   from pyramid.response import Response

   def sample_view(request):
       result = render('mypackage:templates/foo.pt',
                       {'foo':1, 'bar':2},
                       request=request)
       response = Response(result)
       response.content_type = 'text/plain'
       return response

Here's an example view configuration which uses a Chameleon ZPT renderer
registered imperatively:

.. code-block:: python
   :linenos:

    # config is an instance of pyramid.config.Configurator

    config.add_view('myproject.views.sample_view',
                    renderer='myproject:templates/foo.pt')

Here's an example view configuration which uses a Chameleon text renderer
registered imperatively:

.. code-block:: python
   :linenos:

    config.add_view('myproject.views.sample_view',
                    renderer='myproject:templates/foo.txt')

.. _chameleon_zpt_templates:

Chameleon ZPT Templates
-----------------------

:term:`Chameleon` is an implementation of :term:`ZPT` (Zope Page
Templates) templating language.  The Chameleon engine complies largely with 
the `Zope Page Template <http://wiki.zope.org/ZPT/FrontPage>`_ template
specification.  However, it is significantly faster than the default
implementation that is represented by ``zope.pagetemplates``.

The language definition documentation for Chameleon ZPT-style
templates is available from `the Chameleon website
<http://chameleon.repoze.org/>`_.

Given a :term:`Chameleon` ZPT template named ``foo.pt`` in a directory
in your application named ``templates``, you can render the template as
a :term:`renderer` like so:

.. code-block:: python
   :linenos:

   from pyramid.view import view_config

   @view_config(renderer='templates/foo.pt')
   def my_view(request):
       return {'foo':1, 'bar':2}

Two built-in renderers exist for :term:`Chameleon` templates.  If the
``renderer`` parameter of a view configuration is an absolute path, a relative
path or :term:`asset specification` which has a final path element with a
filename extension of ``.pt``, the Chameleon ZPT renderer is used.  If the
extension is ``.txt``, the :term:`Chameleon` text renderer is used.  The
behavior of these renderers is the same, except for the engine used to render
the template.

When a Chameleon renderer is used in a view configuration, the view must return
a :term:`Response` object or a Python *dictionary*.  If the view callable with
an associated template returns a Python dictionary, the named template will be
passed the dictionary as its keyword arguments, and the template renderer
implementation will return the resulting rendered template in a response to the
user.  If the view callable returns anything but a Response object or a
dictionary, an error will be raised.

Before passing keywords to the template, the keyword arguments derived from
the dictionary returned by the view are augmented.  The callable object --
whatever object was used to define the view -- will be automatically inserted
into the set of keyword arguments passed to the template as the ``view``
keyword.  If the view callable was a class, the ``view`` keyword will be an
instance of that class.  Also inserted into the keywords passed to the
template are ``renderer_name`` (the string used in the ``renderer`` attribute
of the directive), ``renderer_info`` (an object containing renderer-related
information), ``context`` (the context resource of the view used to render
the template), and ``request`` (the request passed to the view used to render
the template).  ``request`` is also available as ``req`` in Pyramid 1.3+.

.. index::
   single: ZPT template (sample)

A Sample ZPT Template
~~~~~~~~~~~~~~~~~~~~~

Here's what a simple :term:`Chameleon` ZPT template used under
:app:`Pyramid` might look like:

.. code-block:: xml
   :linenos:

    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml"
          xmlns:tal="http://xml.zope.org/namespaces/tal">
    <head>
        <meta http-equiv="content-type" content="text/html; charset=utf-8" />
        <title>${project} Application</title>
    </head>
      <body>
         <h1 class="title">Welcome to <code>${project}</code>, an
	  application generated by the <a
	  href="http://docs.pylonsproject.org/projects/pyramid/current/"
         >pyramid</a> web
	  application framework.</h1>
      </body>
    </html>

Note the use of :term:`Mako` and/or :term:`Genshi` -style ``${replacements}``
above.  This is one of the ways that :term:`Chameleon` ZPT differs from
standard ZPT.  The above template expects to find a ``project`` key in the set
of keywords passed in to it via :func:`~pyramid.renderers.render` or
:func:`~pyramid.renderers.render_to_response`. Typical ZPT attribute-based
syntax (e.g. ``tal:content`` and ``tal:replace``) also works in these
templates.

.. index::
   single: ZPT macros
   single: Chameleon ZPT macros

Using ZPT Macros in Pyramid
~~~~~~~~~~~~~~~~~~~~~~~~~~~

When a :term:`renderer` is used to render a template, :app:`Pyramid` makes at
least two top-level names available to the template by default: ``context``
and ``request``.  One of the common needs in ZPT-based templates is to use
one template's "macros" from within a different template.  In Zope, this is
typically handled by retrieving the template from the ``context``.  But the
context in :app:`Pyramid` is a :term:`resource` object, and templates cannot
usually be retrieved from resources.  To use macros in :app:`Pyramid`, you
need to make the macro template itself available to the rendered template by
passing the macro template, or even the macro itself, *into* the rendered
template.  To do this you can use the :func:`pyramid.renderers.get_renderer`
API to retrieve the macro template, and pass it into the template being
rendered via the dictionary returned by the view.  For example, using a
:term:`view configuration` via a :class:`~pyramid.view.view_config` decorator
that uses a :term:`renderer`:

.. code-block:: python
   :linenos:

   from pyramid.renderers import get_renderer
   from pyramid.view import view_config

   @view_config(renderer='templates/mytemplate.pt')
   def my_view(request):
       main = get_renderer('templates/master.pt').implementation()
       return {'main':main}

Where ``templates/master.pt`` might look like so:

.. code-block:: xml
   :linenos:

    <html xmlns="http://www.w3.org/1999/xhtml"
          xmlns:tal="http://xml.zope.org/namespaces/tal"
          xmlns:metal="http://xml.zope.org/namespaces/metal">
      <span metal:define-macro="hello">
        <h1>
          Hello <span metal:define-slot="name">Fred</span>!
        </h1>
      </span>
    </html>

And ``templates/mytemplate.pt`` might look like so:

.. code-block:: xml
   :linenos:

    <html xmlns="http://www.w3.org/1999/xhtml"
          xmlns:tal="http://xml.zope.org/namespaces/tal"
          xmlns:metal="http://xml.zope.org/namespaces/metal">
      <span metal:use-macro="main.macros['hello']">
        <span metal:fill-slot="name">Chris</span>
      </span>
    </html>

.. index::
   single: Chameleon text templates

.. _chameleon_text_templates:

Chameleon Text Templates
------------------------

:mod:`pyramid_chameleon` also allows for the use of templates which are
composed entirely of non-XML text via :term:`Chameleon`.  To do so,
you can create templates that are entirely composed of text except for
``${name}`` -style substitution points.

Here's an example usage of a Chameleon text template.  Create a file
on disk named ``mytemplate.txt`` in your project's ``templates``
directory with the following contents:

.. code-block:: text

   Hello, ${name}!

Then in your project's ``views.py`` module, you can create a view
which renders this template:

.. code-block:: python
   :linenos:

   from pyramid.view import view_config

   @view_config(renderer='templates/mytemplate.txt')
   def my_view(request):
       return {'name':'world'}

When the template is rendered, it will show:

.. code-block:: text

   Hello, world!

If you'd rather use templates directly within a view callable (without the
indirection of using ``renderer`` in view configuration), see the functions 
in :mod:`pyramid.renderers` for APIs which allow you to render templates
imperatively.

Template Variables provided by Pyramid
--------------------------------------

Pyramid by default will provide a set of variables that are available within
your templates, please see :ref:`renderer_system_values` for more information
about those variables.

Using A Chameleon Macro Name Within a Renderer Name
---------------------------------------------------

At times, you may want to render a macro inside of a Chameleon ZPT template
instead of the full Chameleon ZPT template. To render the content of a
``define-macro`` field inside a Chameleon ZPT template, given a Chameleon
template file named ``foo.pt`` and a macro named ``bar`` defined within it
(e.g. ``<div metal:define-macro="bar">...</div>``), you can configure the
template as a :term:`renderer` like so:

.. code-block:: python
   :linenos:

   from pyramid.view import view_config

   @view_config(renderer='foo#bar.pt')
   def my_view(request):
       return {'project':'my project'}

The above will render only the ``bar`` macro defined within the ``foo.pt``
template instead of the entire template.

.. index::
   single: template renderer side effects

Side Effects of Rendering a Chameleon Template
----------------------------------------------

When a Chameleon template is rendered from a file, the templating
engine writes a file in the same directory as the template file itself
as a kind of cache, in order to do less work the next time the
template needs to be read from disk. If you see "strange" ``.py``
files showing up in your ``templates`` directory (or otherwise
directly "next" to your templates), it is due to this feature.

If you're using a version control system such as Subversion, you
should configure it to ignore these files.  Here's the contents of the
author's ``svn propedit svn:ignore .`` in each of my ``templates``
directories.

.. code-block:: text

   *.pt.py
   *.txt.py

Note that I always name my Chameleon ZPT template files with a ``.pt``
extension and my Chameleon text template files with a ``.txt``
extension so that these ``svn:ignore`` patterns work.

.. index::
   pair: debugging; templates

.. _debug_templates_section:

Nicer Exceptions in Chameleon Templates
---------------------------------------

The exceptions raised by Chameleon templates when a rendering fails
are sometimes less than helpful.  :app:`Pyramid` allows you to
configure your application development environment so that exceptions
generated by Chameleon during template compilation and execution will
contain nicer debugging information.

.. warning:: Template-debugging behavior is not recommended for
             production sites as it slows renderings; it's usually
             only desirable during development.

In order to turn on template exception debugging, you can use an
environment variable setting or a configuration file setting.

To use an environment variable, start your application under a shell
using the ``PYRAMID_DEBUG_TEMPLATES`` operating system environment
variable set to ``1``, For example:

.. code-block:: text

  $ PYRAMID_DEBUG_TEMPLATES=1 bin/pserve myproject.ini

To use a setting in the application ``.ini`` file for the same
purpose, set the ``pyramid.debug_templates`` key to ``true`` within
the application's configuration section, e.g.:

.. code-block:: ini
  :linenos:

  [app:main]
  use = egg:MyProject
  pyramid.debug_templates = true

With template debugging off, a :exc:`NameError` exception resulting
from rendering a template with an undefined variable
(e.g. ``${wrong}``) might end like this:

.. code-block:: text

  File "...", in __getitem__
    raise NameError(key)
  NameError: wrong

Note that the exception has no information about which template was
being rendered when the error occured.  But with template debugging
on, an exception resulting from the same problem might end like so:

.. code-block:: text

    RuntimeError: Caught exception rendering template.
     - Expression: ``wrong``
     - Filename:   /home/fred/env/proj/proj/templates/mytemplate.pt
     - Arguments:  renderer_name: proj:templates/mytemplate.pt
                   template: <PageTemplateFile - at 0x1d2ecf0>
                   xincludes: <XIncludes - at 0x1d3a130>
                   request: <Request - at 0x1d2ecd0>
                   project: proj
                   macros: <Macros - at 0x1d3aed0>
                   context: <MyResource None at 0x1d39130>
                   view: <function my_view at 0x1d23570>

    NameError: wrong

The latter tells you which template the error occurred in, as well as
displaying the arguments passed to the template itself.

.. note::

   Turning on ``pyramid.debug_templates`` has the same effect as using the
   Chameleon environment variable ``CHAMELEON_DEBUG``.  See `Chameleon
   Environment Variables
   <http://chameleon.repoze.org/docs/latest/config.html#environment-variables>`_
   for more information.

.. index::
   single: automatic reloading of templates
   single: template automatic reload

.. _reload_templates_section:

Automatically Reloading Templates
---------------------------------

It's often convenient to see changes you make to a template file
appear immediately without needing to restart the application process.
:app:`Pyramid` allows you to configure your application development
environment so that a change to a template will be automatically
detected, and the template will be reloaded on the next rendering.

.. warning:: Auto-template-reload behavior is not recommended for
             production sites as it slows rendering slightly; it's
             usually only desirable during development.

In order to turn on automatic reloading of templates, you can use an
environment variable, or a configuration file setting.

To use an environment variable, start your application under a shell
using the ``PYRAMID_RELOAD_TEMPLATES`` operating system environment
variable set to ``1``, For example:

.. code-block:: text

  $ PYRAMID_RELOAD_TEMPLATES=1 bin/pserve myproject.ini

To use a setting in the application ``.ini`` file for the same
purpose, set the ``pyramid.reload_templates`` key to ``true`` within the
application's configuration section, e.g.:

.. code-block:: ini
  :linenos:

  [app:main]
  use = egg:MyProject
  pyramid.reload_templates = true

Settings
--------

Chameleon derives additional settings to configure its template renderer. Many
of these settings are optional and only need to be set if they should be
different from the default.  The below values can be present in the ``.ini``
file used to configure the Pyramid application (in the ``app`` section
representing your Pyramid app) or they can be passed directly within the
``settings`` argument passed to a Pyramid Configurator.

``pyramid.reload_templates``

  ``true`` or ``false`` representing whether Chameleon templates should be
  reloaded when they change on disk.  Useful for development to be ``true``.

``pyramid.debug_templates``

  ``true`` or ``false`` representing whether Chameleon templates should be
   have extra debugging info turned on in tracebacks it generates.

Changing the Content-Type of a Chameleon-Renderered Response
------------------------------------------------------------

Here's an example of changing the content-type and status of the
response object returned by a Chameleon-rendered Pyramid view:

.. code-block:: python
   :linenos:

   @view_config(renderer='foo.pt')
   def sample_view(request):
       request.response.content_type = 'text/plain'
       response.status_int = 204
       return response

See :ref:`request_response_attr` for more information.

.. index::
   single: template internationalization
   single: internationalization (of templates)

Chameleon Template Internationalization
---------------------------------------

Chameleon supports internationalized units of text by reusing the translation
facilities provided within Pyramid. See :ref:`i18n_chapter` for a general
description of these facilities.

Translating Template Content
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You need to add a few boilerplate lines to your application's ``setup.py``
file in order to properly generate :term:`gettext` files from your
application's templates.

.. note:: See :ref:`project_narr` to learn about the
  composition of an application's ``setup.py`` file.

In particular, add the ``Babel`` and ``lingua`` distributions to the
``install_requires`` list and insert a set of references to :term:`Babel`
*message extractors* within the call to :func:`setuptools.setup` inside your
application's ``setup.py`` file:

.. code-block:: python
   :linenos:

    setup(name="mypackage",
          # ...
          install_requires = [
                # ...
                'Babel',
                'lingua',
                ],
          message_extractors = { '.': [
                ('**.py',   'lingua_python', None ),
                ('**.pt',   'lingua_xml', None ),
                ]},
          )

The ``message_extractors`` stanza placed into the ``setup.py`` file causes the
Babel message catalog extraction machinery to also consider ``*.pt`` files when
doing message id extraction.

Once this is done you can generate ``.pot`` files derived from your Chameleon
templates (and Python code).  See :ref:`extracting_messages` in the Pyramid
documentation for general information about this.

Chameleon Template Support for Translation Strings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When a Pyramid "translation string" (see :ref:`i18n_chapter`) is used as the
subject of textual rendering by a ``pyramid_chameleon`` template renderer, it
will automatically be translated to the requesting user's language if a
suitable translation exists. This is true of both the ZPT and text variants of
the Chameleon template renderers.

For example, in a Chameleon ZPT template, the translation string
represented by "some_translation_string" in each example below will go
through translation before being rendered:

.. code-block:: xml
   :linenos:

   <span tal:content="some_translation_string"/>

.. code-block:: xml
   :linenos:

   <span tal:replace="some_translation_string"/>

.. code-block:: xml
   :linenos:

   <span>${some_translation_string}</span>

.. code-block:: xml
   :linenos:

   <a tal:attributes="href some_translation_string">Click here</a>

The features represented by attributes of the ``i18n`` namespace of
Chameleon will also consult the :app:`Pyramid` translations.
See
`http://chameleon.repoze.org/docs/latest/i18n.html#the-i18n-namespace
<http://chameleon.repoze.org/docs/latest/i18n.html#the-i18n-namespace>`_.

.. note::

   Unlike when Chameleon is used outside of :app:`Pyramid`, when it
   is used *within* :app:`Pyramid`, it does not support use of the
   ``zope.i18n`` translation framework.  Applications which use
   :app:`Pyramid` should use the features documented in this
   chapter rather than ``zope.i18n``.

You can always disuse this automatic translation and perform a more manual
translation as described in :ref:`performing_a_translation`.

Unit Testing
------------

When you are running unit tests, you will be required to use
``config.include('pyramid_chameleon')`` to add ``pyramid_chameleon`` so that
its renderers are added to the config and can be used.::

    from pyramid import testing
    from pyramid.response import Response
    from pyramid.renderers import render

    # The view we want to test
    def some_view(request):
        return Response(render('mypkg:templates/home.pt', {'var': 'testing'}))

    class TestViews(unittest.TestCase):
        def setUp(self):
            self.config = testing.setUp()
            self.config.include('pyramid_chameleon')

        def tearDown(self):
            testing.tearDown()

        def test_some_view(self):
            from pyramid.testing import DummyRequest
            request = DummyRequest()
            response = some_view(request)
            # templates/home.mako starts with the standard <html> tag for HTML5
            self.assertTrue('<html' in response.body)


More Information
================

.. toctree::
 :maxdepth: 1

 glossary.rst
 api.rst

Reporting Bugs / Development Versions
=====================================

Visit http://github.com/Pylons/pyramid_chameleon to download development or 
tagged versions.

Visit http://github.com/Pylons/pyramid_chameleon/issues to report bugs.

Indices and tables
------------------

* :ref:`glossary`
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
