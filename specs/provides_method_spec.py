#!/usr/bin/env python

"""Specification for how provider methods work."""


from snakeguice import inject, provides, Injector


def describe_provider_methods():

    def describe_providing_an_object_with_no_dependencies():
        class SomeInterface(object): pass
        class SomeImpl(object): pass

        class Module(object):
            @provides(SomeInterface)
            def aSomeInterfaceFactory(self):
                return SomeImpl()

            def configure(self, binder):
                pass

        injector = Injector(Module())
        some_instance = injector.get_instance(SomeInterface)

        def should_return_the_implementation():
            assert isinstance(some_instance, SomeImpl)

    def describe_providing_an_object_with_dependencies():
        class SomeInterface(object): pass

        class SomeImpl(object):

            def __init__(self, other_dep):
                self.other_dep = other_dep

        class SomeOtherDependency(object): pass

        class Module(object):

            @provides(SomeInterface)
            @inject(other_dep=SomeOtherDependency)
            def aSomeInterfaceFactory(self, other_dep):
                return SomeImpl(other_dep)

            def configure(self, binder):
                pass

        injector = Injector(Module())
        some_instance = injector.get_instance(SomeInterface)

        def should_return_the_implementation():
            assert isinstance(some_instance, SomeImpl)

        def should_have_its_dependencies_injected():
            assert isinstance(some_instance.other_dep, SomeOtherDependency)
