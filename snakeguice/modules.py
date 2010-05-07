
class ModuleAdapter(object):
    """Adapts the simple and standard module interfaces to a common one."""

    def __init__(self, module):
        self._module = module

    def configure(self, binder):
        if hasattr(self._module, 'run_configure'):
            self._module.run_configure(binder)
        else:
            self._module.configure(binder)


class Module(object):
    """Base class for all standard modules."""

    def install(self, binder, module):
        """Add another module's bindings to a binder."""
        ModuleAdapter(module).configure(binder)

    def run_configure(self, binder):
        """A hook for intercepting the configure method. Allows different
        module implementations to change the binder passed to configure.
        """
        self.configure(binder)

    def configure(self, binder):
        """A subclass should override this to configure a binder."""
        raise NotImplementedError


class _PrivateModuleWrapper(Module):
    """Exists solely to remove the infinite recursion in Private Modules
    caused by the child injector calling run_configure.
    """

    def __init__(self, module):
        self._module = module

    def configure(self, binder):
        self._module.configure(binder)


class PrivateModule(Module):
    """Module that uses a child injector to isolate bindings."""

    def expose(self, binder, interface, annotation=None):
        """Expose the child injector to the parent inject for a binding."""
        private_module = self
        class Provider(object):
            def get(self):
                return private_module.private_injector.get_instance(
                        interface, annotation)

        self.original_binder.bind(interface, annotated_with=annotation,
                                  to_provider=Provider)

    def run_configure(self, binder):
        self.original_binder = binder
        private_wrapper = _PrivateModuleWrapper(self)
        self.private_injector = binder._injector.create_child(private_wrapper)
