
class Module(object):

    def __init__(self):
        self.binder = None

    def install(self, binder, module):
        module.preconfigure(binder)


class PrivateModule(Module):

    def expose(self, binder, interface, annotation=None):
        private_module = self
        class Provider(object):
            def get(self):
                return private_module.private_injector.get_instance(
                        interface, annotation)

        self.original_binder.bind(interface, annotated_with=annotation,
                                  to_provider=Provider)

    def preconfigure(self, binder):
        self.original_binder = binder
        self.private_injector = binder._injector.create_child(self)
