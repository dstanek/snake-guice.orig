#!/usr/bin/env python

from snakeguice.binder import Binder


class Injector(object):

    parent = None
    binding_map = None
    stage = None

    def __init__(self, modules, parent=None):
        if not hasattr(modules, '__iter__'):
            modules = [modules]
        if parent:
            self.parent = parent
            self.binding_map = parent.binding_map.copy()
            self.stage = parent.stage
        else:
            self.binding_map = {}
        binder = Binder(self)
        for module in modules:
            module.configure(binder)

    def get_binding(self, _class, annotation=None):
        key = (_class, annotation)
        binding = self.binding_map.get(key)
        if not binding:
            key = (_class, None)
            binding = self.binding_map.get(key)
        return binding

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

    def create_object(self, cls):
        if not isinstance(cls, type):
            return cls

        if not hasattr(cls, '__guice__'):
            return cls()

        guice_data = cls.__guice__

        if not guice_data.init:
            instance = cls()
        else:
            kwargs = {}
            for name, _type in guice_data.init.types.items():
                kwargs[name] = self.get_instance(
                        _type, guice_data.init.annotation)
            instance = cls(**kwargs)

        for name, gp in guice_data.properties:
            value = self.get_instance(gp.type, gp.annotation)
            setattr(instance, name, value)

        for name, gm in guice_data.methods:
            kwargs = {}
            for param, _type in gm.types.items():
                kwargs[param] = self.get_instance(_type, gm.annotation)
            getattr(instance, name)(**kwargs)

        return instance

    def create_child(self, modules):
        """Create a new injector that inherits the state from this injector.

        All bindings are inherited. In the future this may become closer to
        child injectors on google-guice.
        """
        injector = Injector(modules, parent=self)
        return injector
