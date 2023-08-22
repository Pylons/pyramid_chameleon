"""Script to pre-compile chameleon templates to the cache.

This script is useful if the time to compile chameleon templates is
unacceptably long. It finds and compiles all templates within a directory,
saving the result in the cache configured via the CHAMELEON_CACHE environment
variable.
"""

import os
import sys
import logging
import optparse
from multiprocessing import Pool

import chameleon.config
from pyramid_chameleon.zpt import PyramidPageTemplateFile

def _compile_one(args):
    fullpath, template_factory, fail_fast = args[0], args[1], args[2]
    try:
        compile_one(fullpath, template_factory)
    except KeyboardInterrupt:
        return dict(path=fullpath, success=False)
    except Exception as e:
        if fail_fast:
            raise
        logging.error('Failed to compile: %s' % fullpath, exc_info=e)
        return dict(path=fullpath, success=False)
    logging.debug('Compiled: %s' % fullpath)
    return dict(path=fullpath, success=True)

def compile_one(fullpath, template_factory=PyramidPageTemplateFile):
    assert chameleon.config.CACHE_DIRECTORY is not None
    template = template_factory(fullpath, macro=None)
    template.cook_check()

def _walk_dir(directory, extensions):
    ret = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.startswith('.'):
                continue
            _, ext = os.path.splitext(filename)
            if ext not in extensions:
                continue
            fullpath = os.path.join(dirpath, filename)
            ret.append(fullpath)
    return ret

def walk_dir(
        directory,
        extensions=frozenset(['.pt']),
        template_factory=PyramidPageTemplateFile,
        fail_fast=False,
        jobs=1
        ):
    pool = Pool(processes=jobs)
    mapped_args = [
        (fullpath, template_factory, fail_fast)
        for fullpath in _walk_dir(directory, extensions)
    ]
    try:
        for result in pool.map(_compile_one, mapped_args):
            yield result
    finally:
        pool.close()
        pool.join()

def precompile(argv=sys.argv):
    parser = optparse.OptionParser(usage="""usage: %prog [options]

Compile chameleon templates, saving the results in the chameleon cache.

The CACHE_DIRECTORY environment variable MUST be set to the directory where the
templates will be stored.

By default the exit code of this script will be 0 if one template was found and
compiled.
""")
    parser.add_option(
            "--fail-fast",
            dest="fail_fast",
            default=False,
            action="store_true",
            help="Exit with non-zero exit code on the first "
                 "template which fails compillation.")
    parser.add_option(
            "--dir",
            dest="dir",
            help="The directory to search for templates. "
                 "Will be recursively searched")
    parser.add_option(
            "--ext",
            dest="exts",
            action="append",
            help="The file extensions to search for, "
                 "can be specified more than once."
                 "The default is to look only for the .pt extension.")
    parser.add_option(
            "--loglevel",
            dest="loglevel",
            help="set the loglevel, see the logging module for possible values",
            default='INFO')
    parser.add_option(
            "--jobs",
            type=int,
            dest="jobs",
            help="set the N compile jobs",
            default=1)
    options, args = parser.parse_args(argv)
    loglevel = getattr(logging, options.loglevel)
    logging.basicConfig(level=loglevel)
    if chameleon.config.CACHE_DIRECTORY is None:
        logging.error(
            'The CHAMELEON_CACHE environment variable must be specified'
        )
        return 1
    if len(args) > 1:
        msg = ' '.join(args[1:])
        logging.error(
            'This command takes only keyword arguments, got: %s' % msg
        )
        return 1
    exts = options.exts
    if not exts:
        exts = ['.pt']
    exts = set(exts)
    success = total = 0
    for f in walk_dir(
            options.dir,
            extensions=exts,
            fail_fast=options.fail_fast,
            jobs=options.jobs
    ):
        total += 1
        if f['success']:
            success += 1
    logging.info('Compiled %s out of %s found templates' % (success, total))
    if not success:
        logging.error(
            "No templates successfully compiled out of %s found" % total
        )
        return 1
    return 0

if __name__ == '__main__': # pragma: no cover
    sys.exit(precompile())
