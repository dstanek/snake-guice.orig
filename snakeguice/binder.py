#!/usr/bin/env python

from snakeguice import errors, providers, scopes


class Key(object):

    def __init__(self, interface, annotation=None):
        self._interface = interface
        self._annotation = annotation

    def __hash__(self):
        return hash((self._interface, self._annotation))

    def __eq__(self, other):
        return (self._interface == other._interface and
                self._annotation == other._annotation)


class Binder(object):

    def __init__(self, injector, binding_map=None):
        self._injector = injector
        self._errors = []
        self._binding_map = binding_map or {}

    def create_child(self, injector=None):
        return Binder(injector or self._injector, self._binding_map.copy())

    def add_error(self, exc, msg):
        self._errors.append(exc(msg))
        #TODO: do something with this

    def bind(self, _class, **kwargs):
        if _class in self._binding_map:
            raise errors.BindingError('baseclass %r already bound' % _class)

        binding = Binding()
        binding.interface = _class
        binding.scope = scopes.NO_SCOPE

        if 'to' in kwargs:
            #TODO: add some validation
            binding.provider = providers.SimpleProvider(self._injector, kwargs['to'])
        elif 'to_provider' in kwargs:
            #TODO: add some validation
            provider = kwargs['to_provider']
            binding.provider = providers.ProviderProvider(
                    self._injector, provider)
        elif 'to_instance' in kwargs:
            #TODO: add some validation
            provider = kwargs['to_instance']
            binding.provider = providers.InstanceProvider(provider)

        if 'annotated_with' in kwargs:
            annotations = kwargs['annotated_with']
            if not isinstance(annotations, list):
                annotations = [annotations]
            binding.annotations = annotations

        if 'in_scope' in kwargs:
            binding.scope = kwargs['in_scope']

        if binding.annotations:
            for annotation in binding.annotations:
                key = Key(binding.interface, annotation)
                self._binding_map[key] = binding
        else:
            key = Key(binding.interface, None)
            self._binding_map[key] = binding

    def get_binding(self, key):
        return self._binding_map.get(key)


class Binding(object):

    def __init__(self):
        self.interface = None
        self.annotations = []
        self.provider = None
        self.scope = None
