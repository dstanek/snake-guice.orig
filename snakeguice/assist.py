import inspect

from snakeguice import inject
from snakeguice.interfaces import Injector
from snakeguice.decorators import GuiceData, GuiceArg, enclosing_frame
from snakeguice.errors import AssistError


def assisted_inject(**kwargs):

    scope = kwargs.get('scope')
    if 'scope' in kwargs:
        del kwargs['scope']

    def _assisted_inject(func):
        if func.__name__ != '__init__':
            raise AssistError('assisted_inject can only be used on __init__s')

        class_locals = enclosing_frame().f_locals

        guice_data = GuiceData.from_class_dict(class_locals)
        guice_data.assisted = True # TODO: I don't like this, but it works for now

        annotations = getattr(func, '__guice_annotations__', {})

        guice_data.init = dict((k, GuiceArg(v, annotations.get(k)))
                                for k, v in kwargs.items())

        return func

    return _assisted_inject


assisted = object()


def AssistProvider(cls):
    guice_data = GuiceData.from_class(cls)
    if not getattr(guice_data, 'assisted', False):
        raise AssistError('AssistProvider can only by used on '
                '@assisted_inject-ed classes')

    class _AssistProvider(object):

        @inject(injector=Injector)
        def __init__(self, injector):
            self._injector = injector

        def get(self):
            return build_factory(self._injector, cls)

    return _AssistProvider


def build_factory(injector, cls):
    guice_data = GuiceData.from_class(cls)

    providers = {}
    for name, guicearg in guice_data.init.items():
        providers[name] = injector.get_provider(guicearg.datatype,
                                                guicearg.annotation)

    all_args = inspect.getargspec(cls.__init__).args[1:]
    needed_args = set(all_args) - set(providers.keys())

    class DynamicFactory(object):

        def create(self, **kwargs):
            if set(kwargs.keys()) - needed_args:
                raise TypeError('TODO: error message here about too many values')

            for name, provider in providers.items():
                kwargs[name] = provider.get()
            return cls(**kwargs)

    return DynamicFactory()
