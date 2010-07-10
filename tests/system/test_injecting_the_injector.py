from snakeguice import create_injector, inject
from snakeguice.interfaces import Injector


class ISomething(object):
    """An interface."""


class Something(object):
    """Something a little more concrete."""


class SomethingProvider(object):

    @inject(injector=Injector)
    def __init__(self, injector):
        self.injector = injector

    def get(self):
        return self.injector.get_instance(Something)


class Module(object):

    def configure(self, binder):
        binder.bind(ISomething, to_provider=SomethingProvider)


def test():
    injector = create_injector([Module()])
    something = injector.get_instance(ISomething)
    assert isinstance(something, Something)

    something = injector.get_instance(SomethingProvider)
    assert something.injector is injector
