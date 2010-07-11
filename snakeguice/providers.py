"""Providers used in the binding process."""

# pylint: disable-msg=C0111
#         providers are so small that we can safely omit doc comments

from snakeguice.decorators import inject
from snakeguice.interfaces import Injector


def create_simple_provider(cls):
    class DynamicSimpleProvider(object):

        @inject(injector=Injector)
        def __init__(self, injector):
            self._injector = injector

        def get(self):
            return self._injector.create_object(cls)

    return DynamicSimpleProvider


def create_instance_provider(obj):
    class DynamicInstanceProvider(object):

        def get(self):
            return obj

    return DynamicInstanceProvider
