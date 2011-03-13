#!/usr/bin/env python

"""Specification for how snake-guice handles injection."""


from snakeguice import Injector, inject, annotate


def describe_injecting_a_class():

    class IClass(object):
        pass

    class MyClass(object):
        pass

    class DomainObject(object):

        @inject(class_=IClass)
        def __init__(self, class_):
            self.class_ = class_

    class Module(object):

        def configure(self, binder):
            binder.bind(IClass, to_instance=MyClass)

    injector = Injector(Module())
    instance = injector.get_instance(DomainObject)

    def a_class_object_should_have_been_injected():
        assert instance.class_ is MyClass

    def describe_injecting_a_subclass():
        class SubDomainObject(DomainObject):
            pass

        def a_class_object_should_have_been_injected():
            assert instance.class_ is MyClass

