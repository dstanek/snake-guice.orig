#TODO: define simple and standard modules in the documentation

from nose.tools import raises
from mock import Mock
from contextlib import nested

from snakeguice.modules import Module


def given_a_standard_module():

    class StandardModule(Module): pass
    mod = StandardModule()
    binder = Mock()

    def when_installing_a_simple_module():
        simple_module = Mock(spec=['configure'])
        mod.install(binder, simple_module)

        def then_the_simple_modules_configure_method_is_called():
            assert simple_module.configure.called

        def then_the_binder_is_pass_into_the_configure_method():
            assert simple_module.configure.call_args == ((binder,), {})

    def when_installing_a_standard_module():

        class FakeModule(Module):
            calls = []

            def run_configure(self, binder):
                self.calls.append(('run_configure', binder))
                return super(FakeModule, self).run_configure(binder)

            def configure(self, binder):
                self.calls.append(('configure', binder))

        standard_module = FakeModule()
        mod.install(binder, standard_module)

        def then_the_run_configure_method_is_called_with_binder():
            assert ('run_configure', binder) in FakeModule.calls

        def then_the_configure_method_is_called_with_the_same_binder():
            assert ('configure', binder) in FakeModule.calls

    def when_not_overriding_configure():

        @raises(NotImplementedError)
        def then_an_NotImplementedError_should_be_raised():
            mod.configure(None)
