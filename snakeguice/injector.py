#!/usr/bin/env python

import inspect

from snakeguice.binder import Binder, Key
from snakeguice.decorators import GuiceData as _GuiceData


class ProvidesBinderHelper(object):

    def __init__(self, injector):
        self._injector = injector

    def bind_providers(self, module, binder):
        members = [m for m in inspect.getmembers(module)
                   if inspect.ismethod(m[1])]
        for name, method in members:
            if hasattr(method.im_func, '__guice_provides__'):
                type = method.__guice_provides__
                provider = self._build_provider(module, type, method)
                binder.bind(type, to_provider=provider)

    def _build_provider(self, module, type, method):
        helper_self = self
        class GenericProvider(object):
            def get(self):
                kwargs = {}
                method_name = method.__name__
                if hasattr(module, '__guice__'):
                    injectable_args = module.__guice__.methods.get(method_name, {})
                    for name, guicearg in injectable_args.items():
                        kwargs[name] = helper_self._injector.get_instance(
                                guicearg.datatype, guicearg.annotation)
                return method(**kwargs)
        return GenericProvider


class Injector(object):

    def __init__(self, modules, binder=None, stage=None):
        if not hasattr(modules, '__iter__'):
            modules = [modules]

        self._binder = binder or Binder(self)
        self._stage = stage

        provides_helper = ProvidesBinderHelper(self)
        for module in modules:
            module.configure(self._binder)
            open('/tmp/dstanek.log', 'a').write('M %s\n' % (module))
            provides_helper.bind_providers(module, self._binder)

    def get_binding(self, key):
        return self._binder.get_binding(key)

    def get_instance(self, cls, annotation=None):
        key = Key(cls, annotation)
        binding = self.get_binding(key)
        if binding:
            provider = binding.scope.scope(key, binding.provider)
            return provider.get()
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
        if not hasattr(cls, '__guice__'):
            return cls()

        guice_data = self._get_guice_data(cls)

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

    def _get_guice_data(self, cls):
        guice_data = _GuiceData()

        for cls in cls.__mro__[-1::-1]:
            if hasattr(cls, '__guice__'):
                for name, method in cls.__guice__.methods.items():
                    guice_data.methods[name] = method

        if hasattr(cls, '__guice__'):
            guice_data.init = cls.__guice__.init

        return guice_data
