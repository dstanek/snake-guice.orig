import os

from snakeguice.ext import ParameterExtension


IConfig = object()


class Config(ParameterExtension):
    interface = IConfig


class ConfigParserLoader(object):

    def __init__(self, filename):
        self.filename = filename
        self.short_name = os.path.basename(filename)

    def bind_configuration(self, binder):
        from ConfigParser import SafeConfigParser
        parser = SafeConfigParser()
        parser.read(self.filename)
        for section in parser.sections():
            for option in parser.options(section):
                getter = parser.get
                value = getter(section, option)
                annotation = '%s:%s:%s' % (self.short_name, section, option)
                binder.bind(IConfig,
                            to_instance=value,
                            annotated_with=annotation)
