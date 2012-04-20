from os.path import join as joinpath, dirname
from setuptools import setup, Command

from snakeguice import __pkginfo__ as pkg


cmdclass = {}

try:
    from pylint import lint as linter

    class LintCommand(Command):
        description = "Run PyLint over the project"
        user_options = [
                ('report', 'r', 'Print PyLint reports (default: false)'),
                ('rcfile=', 'f', 'PyLint config file'),
        ]

        def initialize_options(self):
            self.report = False
            self.rcfile = None

        def finalize_options(self):
            if not self.rcfile:
                self.rcfile = joinpath(dirname(__file__), 'pylint.cfg')
            self.report = bool(self.report)

        def run(self):
            args = ['--rcfile', self.rcfile]
            if not self.report:
                args.append('-rn')

            ##pkgs = list(set(p.split(".")[0] for p in options.setup.packages))
            pkgs = ['snakeguice']
            linter.Run(args + pkgs)

    cmdclass['lint'] = LintCommand

except ImportError:
    """Pylint is not installed."""

try:
    import nose

    class TestsCommand(Command):
        description = "Run unit tests with nose"
        user_options = [('coverage', 'c', 'Generate figleaf sections.')]

        def initialize_options(self):
            self.coverage = None

        def finalize_options(self):
            self.coverage = bool(self.coverage)

        def run(self):
            if self.coverage:
                import figleaf
                figleaf.start()
            nose.run(argv=['nosetests'])
            if self.coverage:
                figleaf.stop()
                figleaf.write_coverage('.figleaf')

    cmdclass['tests'] = TestsCommand

except ImportError:
    """Nose is not installed."""

try:
    import mote.runner

    class SpecsCommand(Command):
        description = "Run specs with mote"
        user_options = [('quiet', 'q', "Don't print the specification")]

        def initialize_options(self):
            self.quiet = None

        def finalize_options(self):
            self.quiet = bool(self.quiet)

        def run(self):
            sys.argv.append('specs')
            mote.runner.main()

    cmdclass['specs'] = SpecsCommand

except ImportError:
    """mote is not installed."""

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
    download_url=pkg.download_url,
    cmdclass=cmdclass
)
