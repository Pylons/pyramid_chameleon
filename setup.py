import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'Chameleon',
    ]

docs_extras = [
    'Sphinx',
    'docutils',
    'repoze.sphinx.autointerface',
    ]

testing_extras = [
    'nose',
    'nose-selecttests',
    'coverage',
    'virtualenv', # for scaffolding tests
    ]

setup(name='pyramid_chameleon',
      version='0.1',
      description='pyramid_chameleon',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Intended Audience :: Developers",
        "License :: Repoze Public License",
        "Topic :: Text Processing :: Markup :: XML",
        "Topic :: Text Processing :: Markup :: HTML",
        ],
      author="reed@koansys.com, Pylons & Pyramid community",
      author_email="pylons-discuss@googlegroups.com",
      url="https://github.com/Pylons/pyramid_chameleon",
      license="BSD-derived (http://www.repoze.org/LICENSE.txt)",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      extras_require = {
          'testing':testing_extras,
          'docs':docs_extras,
          },
      test_suite="pyramid_chameleon",
      entry_points="""\
      """,
      )
