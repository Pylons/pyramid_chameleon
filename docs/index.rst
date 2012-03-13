==============
pyramid_chameleon
==============

Overview
========

:term:`pyramid_chameleon` is a set of bindings that make templates written for the
:term:`Chameleon` templating system work under the :term:`Pyramid` web framework.

Installation
============

Install using setuptools, e.g. (within a virtualenv)::

  $ $myvenv/bin/easy_install pyramid_chameleon

Setup
=====

There are two ways to make sure that ``pyramid_chameleon`` is active.  They
are completely equivalent:

#) Use the ``includeme`` function via ``config.include``::

    config.include('pyramid_chameleon')

#) If you're using ``pyramid_zcml`` instead of imperative configuration,
   wnsure that some ZCML file with an analogue of the following contents is
   executed by your Pyramid application::

    <include package="pyramid_chameleon"/>

Once activated, the following happens:

#) Files with the ``.pt`` extension are considered to be
   :term:`Chameleon` templates.

#) The :func:`pyramid_chameleon.add_chameleon_search_path` directive is added to
   the :term:`configurator` instance.

#) The :func:`pyramid_chameleon.add_chameleon_extension` directive is added to the
   :term:`configurator` instance.

#) The :func:`pyramid_chameleon.get_chameleon_environment` directive is added to the
   :term:`configurator` instance.

To setup the chameleon search path either one of the following steps must be taken:

#) Add ``chameleon.directories`` to your ``.ini`` settings file using the pyramid
   asset spec::

     chameleon.directories = yourapp:templates

#) Or Alternatively by using the ``add_chameleon_search_path`` directive
   attached to your application's :term:`configurator` instance also using
   the pyramid asset spec::

     config.add_chameleon_search_path("yourapp:templates")

.. warning::

    If you do not explicitly configure your chameleon search path it will
    default to the root of your application.  If configured in this way all
    subsequent paths will need to be specified relative to the root of your
    application's package.  For example:

    Without the search path configured:

    .. code-block:: text

        @view_config(renderer='templates/mytemplate.pt')

    With the search path configured:

    .. code-block:: text

       @view_config(renderer='mytemplate.pt')

Usage
=====

Once :term:`pyramid_chameleon` been activated ``.pt`` templates
can be loaded either by looking up names that would be found on
the :term:`Chameleon` search path or by looking up asset specifications.

Template Lookups
----------------

The default lookup mechanism for templates uses the :term:`Chameleon`
search path. (specified with ``chameleon.directories`` or by using the
add_chameleon_search_path directive on the :term:`configurator` instance.)

Rendering :term:`Chameleon` templates with a view like this is typically
done as follows (where the ``templates`` directory is expected to
live in the search path):

.. code-block:: python
 :linenos:

 from pyramid.view import view_config

 @view_config(renderer='mytemplate.pt')
 def myview(request):
     return {'foo':1, 'bar':2}

Rendering templates outside of a view (and without a request) can be
done using the renderer api:

.. code-block:: python
 :linenos:

 from pyramid.renderers import render_to_response
 render_to_response('mytemplate.pt', {'foo':1, 'bar':2})


Asset Specification Lookups
---------------------------

Looking up templates via asset specification is a feature specific
to :term:`Pyramid`.  For further info please see `Understanding
Asset Specifications
<http://docs.pylonsproject.org/projects/pyramid/1.0/narr/assets.html#understanding-asset-specifications>`_.
Overriding templates in this style uses the standard
`pyramid asset overriding technique
<http://docs.pylonsproject.org/projects/pyramid/1.0/narr/assets.html#overriding-assets>`_.


Settings
========

Chameleon derives additional settings to configure its template renderer. Many
of these settings are optional and only need to be set if they should be
different from the default.  The below values can be present in the ``.ini``
file used to configure the Pyramid application (in the ``app`` section
representing your Pyramid app) or they can be passed directly within the
``settings`` argument passed to a Pyramid Configurator.

reload_templates

  ``true`` or ``false`` representing whether Chameleon templates should be
  reloaded when they change on disk.  Useful for development to be ``true``.

chameleon.directories

  A list of directory names or a newline-delimited string with each line
  representing a directory name.  These locations are where Chameleon will
  search for templates.  Each can optionally be an absolute resource
  specification (e.g. ``package:subdirectory/``).

chameleon.input_encoding

  The input encoding of templates.  Defaults to ``utf-8``.


chameleon.extensions

  A list of extension objects or a newline-delimited set of dotted import
  locations where each line represents an extension.

chameleon.filters

  A dictionary mapping filter name to filter object, or a newline-delimted
  string with each line in the format ``name = dotted.name.to.filter``
  representing Chameleon filters.


Creating a Chameleon ``Pyramid`` Project
=====================================

NB: **To Be Done**

After you've got ``pyramid_chameleon`` installed, you can invoke one of the
following commands to create a Chameleon-based Pyramid project.

On Pyramid 1.0, 1.1, or 1.2::

  $ $myvenv/bin/paster create -t pyramid_chameleon_starter myproject

On Pyramid 1.3::

  $ $myenv/bin/pcreate -s pyramid_chameleon_starter myproject

After it's created, you can visit the ``myproject`` directory and run
``setup.py develop``.  At that point you can start the application like any
other Pyramid application.

This is a good way to see a working Pyramid application that uses Chameleon, even
if you wind up not using the result.


More Information
================

.. toctree::
 :maxdepth: 1

 glossary.rst
 api.rst

Reporting Bugs / Development Versions
=====================================

Visit http://github.com/Pylons/pyramid_chameleon to download development or tagged
versions.

Visit http://github.com/Pylons/pyramid_chameleon/issues to report bugs.

Indices and tables
------------------

* :ref:`glossary`
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
