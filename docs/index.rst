=================
pyramid_chameleon
=================

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

There are several ways to make sure that ``pyramid_chameleon`` is active.  They
are completely equivalent:

#) Add pyramid_chameleon to the `pyramid.includes` section of your applications
   main configuration section::

    [app:main]
    ...
    pyramid.includes = pyramid_chameleon


#) Use the ``includeme`` function via ``config.include``::

    config.include('pyramid_chameleon')

#) If you're using ``pyramid_zcml`` instead of imperative configuration,
   wnsure that some ZCML file with an analogue of the following contents is
   executed by your Pyramid application::

    <include package="pyramid_chameleon"/>

Once activated, files with the ``.pt`` extension are considered to be
:term:`Chameleon` templates.

Usage
=====

Once :term:`pyramid_chameleon` been activated ``.pt`` templates
can be loaded either by looking up names that would be found on
the :term:`Chameleon` search path or by looking up asset specifications.



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




Creating a Chameleon ``Pyramid`` Project
========================================

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


More Information
================

.. toctree::
 :maxdepth: 1

 templates.rst
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
