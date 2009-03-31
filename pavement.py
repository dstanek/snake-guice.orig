import os
import sys
from paver.defaults import *
import paver
import paver.runtime

sys.path.insert(0, paver.runtime.path.getcwd())

from snakeguice import __pkginfo__ as pkg


options(
        setup=Bunch(
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
    def test():
        """Run unit tests with Nose."""
        if options.get('test', {}).get('coverage', 0):
            import figleaf
            figleaf.start()
        nose.run(argv=['nosetests'])
        if options.get('test', {}).get('coverage', 0):
            figleaf.stop()
            figleaf.write_coverage('.figleaf')
except ImportError:
    """Nose is not installed."""
