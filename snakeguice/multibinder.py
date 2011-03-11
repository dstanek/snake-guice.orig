from snakeguice import providers
from snakeguice.annotation import Annotation
from snakeguice.binder import Key
from snakeguice.decorators import inject
from snakeguice.interfaces import Injector
from snakeguice.errors import MultiBindingError


class _MultiBinder(object):

    def __init__(self, binder, interface):
        self._binder = binder
        self._interface = interface
        self._provider = self._get_or_create_provider()

    def _get_or_create_provider(self):
        key = Key(self.multibinding_type(self._interface))
        binding = self._binder.get_binding(key)
        if not binding:
            self._binder.bind(self.multibinding_type(self._interface),
                    to_provider=self._create_provider())
            binding = self._binder.get_binding(key)
        return binding.provider

    def _dsl_to_provider(self, to, to_provider, to_instance):
        if to:
            #TODO: add some validation
            return providers.create_simple_provider(to)
        elif to_provider:
            #TODO: add some validation
            return to_provider
        elif to_instance:
            #TODO: add some validation
            return providers.create_instance_provider(to_instance)
        else:
            raise MultiBindingError('incorrect arguments to %s.add_binding'
                    % self.__class__.__name__)


class List(Annotation):
    """Used for binding lists."""


class ListBinder(_MultiBinder):

    multibinding_type = List

    def add_binding(self, to=None, to_provider=None, to_instance=None):
        provider = self._dsl_to_provider(to, to_provider, to_instance)
        self._provider.add_provider(provider)

    def _create_provider(self):
        class DynamicMultiBindingProvider(object):
            providers = []

            @inject(injector=Injector)
            def __init__(self, injector):
                self._injector = injector

            @classmethod
            def add_provider(cls, provider):
                cls.providers.append(provider)

            def get(self):
                return [self._injector.get_instance(p).get()
                        for p in self.providers]

        return DynamicMultiBindingProvider


class Dict(Annotation):
    """Used for binding dictionaries."""


class DictBinder(_MultiBinder):

    multibinding_type = Dict

    def add_binding(self, key, to=None, to_provider=None, to_instance=None):
        provider = self._dsl_to_provider(to, to_provider, to_instance)
        self._provider.add_provider(key, provider)

    def _create_provider(self):
        binder_self = self

        class DynamicMultiBindingProvider(object):
            providers = {}

            @inject(injector=Injector)
            def __init__(self, injector):
                self._injector = injector

            @classmethod
            def add_provider(cls, key, provider):
                if key in cls.providers:
                    msg = ('duplicate binding for %r in Dict(%s) found'
                            % (key, binder_self.interface.__class__.__name__))
                    raise MultiBindingError(msg)
                cls.providers[key] = provider

            def get(self):
                return dict([(k, self._injector.get_instance(p).get())
                        for k, p in self.providers.items()])

        return DynamicMultiBindingProvider
