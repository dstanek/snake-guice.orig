import os
from ConfigParser import SafeConfigParser

from snakeguice.annotation import Annotation


class Config(Annotation):
    """Annotation for ConfigParser style config files."""


class ConfigParserLoader(object):

    def __init__(self, filename):
        self.filename = filename
        self.short_name = os.path.basename(filename)

    def bind_configuration(self, binder):
        parser = SafeConfigParser()
        parser.read(self.filename)
        for section, option, value in _iterate_parser(parser):
            annotation = Config('%s:%s:%s'
                                % (self.short_name, section, option))
            binder.bind(annotation, to_instance=value)


def _iterate_parser(parser):
    for section in parser.sections():
        for option in parser.options(section):
            value = parser.get(section, option)
            yield section, option, value
