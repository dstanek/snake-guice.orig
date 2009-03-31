#!/usr/bin/env python


from snakeguice import errors, providers, scopes


class Binder(object):

    def __init__(self, injector):
        self._injector = injector
        self._errors = []

    def add_error(self, exc, msg):
        self._errors.append(exc(msg))
        #TODO: do something with this

    def bind(self, _class, **kwargs):
        if _class in self._injector.binding_map:
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
        elif 'to_eager_singleton' in kwargs:
            #TODO: add some validation
            cls = kwargs['to_eager_singleton']
            binding.provider = providers.SimpleProvider(self._injector, cls)
            binding.scope = scopes.SINGLETON
        elif 'to_lazy_singleton' in kwargs:
            #TODO: add some validation
            cls = kwargs['to_lazy_singleton']
            binding.provider = providers.SimpleProvider(self._injector, cls)
            binding.scope = scopes.SINGLETON

        if 'annotated_with' in kwargs:
            annotations = kwargs['annotated_with']
            if not isinstance(annotations, list):
                annotations = [annotations]
            binding.annotations = annotations

        if 'in_scope' in kwargs:
            binding.scope = kwargs['in_scope']

        if binding.annotations:
            for annotation in binding.annotations:
                key = (binding.interface, annotation)
                self._injector.binding_map[key] = binding
        else:
            key = (binding.interface, None)
            self._injector.binding_map[key] = binding

    def get_binding(self, _class, annotation=None):
        key = (_class, annotation)
        binding = self._injector.binding_map.get(key)
        if not binding:
            key = (_class, None)
            binding = self._injector.binding_map.get(key)
        return binding


class Binding(object):

    def __init__(self):
        self.interface = None
        self.annotations = []
        self.provider = None
        self.scope = None
