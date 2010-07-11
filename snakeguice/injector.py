import inspect

from snakeguice.binder import Binder, Key
from snakeguice.decorators import GuiceData as _GuiceData, inject
from snakeguice.modules import ModuleAdapter
from snakeguice.interfaces import Injector as IInjector


class ProvidesBinderHelper(object):

    def bind_providers(self, module, binder):
        members = [m for m in inspect.getmembers(module)
                   if inspect.ismethod(m[1])]
        for name, method in members:
            if hasattr(method.im_func, '__guice_provides__'):
                type = method.__guice_provides__
                provider = self._build_provider(module, type, method)
                binder.bind(type, to_provider=provider)

    def _build_provider(self, module, type, method):

        class GenericProvider(object):

            @inject(injector=IInjector)
            def __init__(self, injector):
                self._injector = injector

            def get(self):
                kwargs = {}
                method_name = method.__name__
                guice_data = _GuiceData.from_class(module.__class__)
                injectable_args = guice_data.methods.get(method_name, {})
                for name, guicearg in injectable_args.items():
                    kwargs[name] = self._injector.get_instance(
                            guicearg.datatype, guicearg.annotation)
                return method(**kwargs)

        return GenericProvider


class Injector(object):

    def __init__(self, modules=None, binder=None, stage=None):
        if modules is None:
            modules = []
        elif not hasattr(modules, '__iter__'):
            modules = [modules]

        if binder:
            self._binder = binder.create_child()
        else:
            self._binder = Binder()

        self._stage = stage

        self.add_modules(modules)

    def add_modules(self, modules):
        provides_helper = ProvidesBinderHelper()
        for module in modules:
            ModuleAdapter(module).configure(self._binder)
            provides_helper.bind_providers(module, self._binder)

    def get_binding(self, key):
        return self._binder.get_binding(key)

    def get_provider(self, cls, annotation=None):
        injector = self

        class DynamicProvider(object):

            def get(self):
                return injector.get_instance(cls, annotation)

        return DynamicProvider()

    def get_instance(self, cls, annotation=None):
        if cls is IInjector: # TODO: i don't like this, but it works for now
            return self

        key = Key(cls, annotation)
        binding = self.get_binding(key)
        if binding:
            provider = binding.scope.scope(key, binding.provider)
            provider_inst = self.get_instance(provider)
            return provider_inst.get()
        else:
            return self.create_object(cls)

    def create_child(self, modules):
        """Create a new injector that inherits the state from this injector.

        All bindings are inherited. In the future this may become closer to
        child injectors on google-guice.
        """
        binder = self._binder.create_child()
        return Injector(modules, binder=binder, stage=self._stage)

    def create_object(self, cls):
        guice_data = _GuiceData.composite_from_class(cls)

        if not guice_data.init:
            instance = cls()
        else:
            kwargs = {}
            for name, guicearg in guice_data.init.items():
                kwargs[name] = self.get_instance(guicearg.datatype,
                                                 guicearg.annotation)
            instance = cls(**kwargs)

        for name, gm in guice_data.methods.items():
            kwargs = {}
            for param, guicearg in gm.items():
                kwargs[param] = self.get_instance(guicearg.datatype,
                                                  guicearg.annotation)
            getattr(instance, name)(**kwargs)

        return instance


def create_injector(modules):
    """Factory for creating Injector instances."""
    return Injector(modules)
