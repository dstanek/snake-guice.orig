#!/usr/bin/env python

"""Specification for how snake-guice handles injection."""

from snakeguice import inject, annotate, Injector
from snakeguice.config import Config, ConfigParserLoader


def describe_injecting_configuration_with_the_default_adapter():

    class MyWebService(object):

        @inject(ipaddress=Config('config.ini:webservice:ipaddress'),
                port=Config('config.ini:webservice:port'))
        def __init__(self, ipaddress, port):
            self.ipaddress = ipaddress
            self.port = port

    class ConfigModule(object):

        def configure(self, binder):
            config_loader = ConfigParserLoader('specs/config.ini')
            config_loader.bind_configuration(binder)

    injector = Injector(ConfigModule())
    webservice = injector.get_instance(MyWebService)

    def config_values_are_being_injected():
        assert webservice.ipaddress == '127.0.0.1'
        assert webservice.port == '9999'
