#!/usr/bin/env python

from snakeguice.binder import Binder
from snakeguice.decorators import GuiceData as _GuiceData


class Injector(object):

    def __init__(self, modules, binder=None, stage=None):
        if not hasattr(modules, '__iter__'):
            modules = [modules]

        self._binder = binder or Binder(self)
        self._stage = stage

        for module in modules:
            module.configure(self._binder)

    def get_binding(self, _class, annotation=None):
        return self._binder.get_binding(_class, annotation)

    def get_instance(self, cls, annotation=None):
        key = (cls, annotation)
        binding = self.get_binding(*key)
        if binding:
            provider = binding.scope.scope(key, binding.provider)
            impl_class = provider.get()
        else:
            impl_class = cls

        instance = self.create_object(impl_class)
        return instance

    def create_child(self, modules):
        """Create a new injector that inherits the state from this injector.

        All bindings are inherited. In the future this may become closer to
        child injectors on google-guice.
        """
        binder = self._binder.create_child()
        return Injector(modules, binder=binder, stage=self._stage)

    def create_object(self, cls):
        if not isinstance(cls, type):
            return cls

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
