import os
import sys
from paver.easy import *
import paver
from paver.setuputils import setup

sys.path.insert(0, os.path.dirname(__file__))

from snakeguice import __pkginfo__ as pkg


setup(
    name=pkg.libname,
    version=pkg.version,
    license=pkg.license,
    packages=pkg.packages,
    author=pkg.author,
    author_email=pkg.author_email,
    description=pkg.short_desc,
    long_description=pkg.long_desc,
    classifiers=pkg.classifiers,
    url=pkg.url,
    download_url=pkg.download_url
)


#
# Generic Tasks
#


@task
@needs(['generate_setup', 'minilib', 'setuptools.command.sdist'])
def sdist():
    """Overrides sdist to make sure that our setup.py is generated."""


try:
    from pylint import lint as linter
    @task
    @cmdopts([('msg-only', 'm', 'Only generate messages (no reports)')])
    def lint():
        """Check the module you're building with pylint."""
        build_dir = paver.runtime.path.getcwd()
        args = ['--rcfile', build_dir / "pylint.cfg"]
        if options.get('lint', {}).get('msg_only', 0):
            args.append('-rn')

        pkgs = list(set(p.split(".")[0] for p in options.setup.packages))
        args += pkgs
        linter.Run(args)
except ImportError:
    """Pylint is not installed."""


try:
    import nose
    @task
    @cmdopts([('coverage', 'c', 'Generate figleaf sections.')])
    def tests():
        """Run unit tests with Nose."""
        if options.get('tests', {}).get('coverage', 0):
            import figleaf
            figleaf.start()
        nose.run(argv=['nosetests'])
        if options.get('tests', {}).get('coverage', 0):
            figleaf.stop()
            figleaf.write_coverage('.figleaf')
except ImportError:
    """Nose is not installed."""


try:
    import mote
    @task
    @cmdopts([('quiet', 'q', "Don't print the specification")])
    def specs():
        """Run specs with mote."""
        sys.argv.append('specs')
        mote.main()
except ImportError:
    """mote is not installed."""


@task
@needs(['tests', 'specs'])
def all_tests():
    """Run unit tests and specs."""
