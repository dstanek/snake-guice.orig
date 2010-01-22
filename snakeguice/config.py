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
        from ConfigParser import SafeConfigParser
        parser = SafeConfigParser()
        parser.read(self.filename)
        for section, option, value in _iterate_parser(parser):
            annotation = Config('%s:%s:%s' % (self.short_name, section, option))
            self._add_binding_to_binder(binder, Config, value, annotation)

    def _add_binding_to_binder(self, binder, interface, value, annotation):
        binder.bind(interface, to_instance=value, annotated_with=annotation)


def _iterate_parser(parser):
    for section in parser.sections():
        for option in parser.options(section):
	    value = parser.get(section, option)
            yield section, option, value
