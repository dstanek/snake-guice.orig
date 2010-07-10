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

    def __ne__(self, other):
        return not self == other


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
        key = Key(interface=_class, annotation=kwargs.get('annotated_with'))

        binding = Binding()
        binding.key = key
        binding.scope = kwargs.get('in_scope', scopes.NO_SCOPE)

        if key in self._binding_map:
            raise errors.BindingError('baseclass %r already bound' % _class)

        if 'to' in kwargs:
            #TODO: add some validation
            binding.provider = providers.SimpleProvider(
                    self._injector, kwargs['to'])
        elif 'to_provider' in kwargs:
            #TODO: add some validation
            provider = kwargs['to_provider']
            binding.provider = providers.ProviderProvider(
                    self._injector, provider)
        elif 'to_instance' in kwargs:
            #TODO: add some validation
            provider = kwargs['to_instance']
            binding.provider = providers.InstanceProvider(provider)

        self._binding_map[key] = binding

    def get_binding(self, key):
        return self._binding_map.get(key)


class Binding(object):

    def __init__(self):
        self.key = None
        self.provider = None
        self.scope = None
