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


class _EmptyBinder(object):

    def get_binding(self, key):
        return None


class Binder(object):

    def __init__(self, parent=None):
        self._parent = parent or _EmptyBinder()
        self._errors = []
        self._binding_map = {}

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
            if not isinstance(kwargs['to'], type):
                raise errors.BindingError("'to' requires a new-style class")

            binding.provider = providers.create_simple_provider(kwargs['to'])

        elif 'to_provider' in kwargs:
            #TODO: add some validation
            provider = kwargs['to_provider']
            binding.provider = provider

        elif 'to_instance' in kwargs:
            if not isinstance(kwargs['to_instance'], object):
                raise errors.BindingError(
                    "'to_instance' requires an instance of a new-style class")

            provider = kwargs['to_instance']
            binding.provider = providers.create_instance_provider(provider)

        self._binding_map[key] = binding

    def get_binding(self, key):
        return self._binding_map.get(key) or self._parent.get_binding(key)

    def create_child(self):
        return Binder(self)


class Binding(object):

    def __init__(self):
        self.key = None
        self.provider = None
        self.scope = None
