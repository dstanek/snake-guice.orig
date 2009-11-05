#!/usr/bin/env python

"""Specification for how snake-guice handles injection."""

from snakeguice import inject, Injected, Injector, Config
from snakeguice.config import ConfigParserLoader


def describe_injecting_configuration_with_the_default_adapter():

    class MyLogger(object):

        @inject(filename=Config('config.ini:logger:filename'),
                loglevel=Config('config.ini:logger:loglevel'))
        def __init__(self, filename=Injected, loglevel=Injected):
            self.filename = filename
            self.loglevel = loglevel

    class ConfigModule(object):

        def configure(self, binder):
            config_loader = ConfigParserLoader('specs/config.ini')
            config_loader.bind_configuration(binder)

    injector = Injector(ConfigModule())
    logger = injector.get_instance(MyLogger)

    def config_values_are_being_injected():
        assert logger.filename == '/var/log/guice.log'
        assert logger.loglevel == 'INFO'
