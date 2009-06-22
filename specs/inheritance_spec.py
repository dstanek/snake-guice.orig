#!/usr/bin/env python

"""Specification for how snake-guice handles inherited classes."""


from snakeguice import Injector, inject, Injected


class Data(object): pass
class OldData(object): pass
class NewData(object): pass


class Module(object):
    def configure(self, binder):
        binder.bind(Data, annotated_with='old', to=OldData)
        binder.bind(Data, annotated_with='new', to=NewData)


def describe_inheriting_an_attribute():
    class Parent(object):
        parent_attr = inject(Data, annotation='old')

    class Child(Parent):
        child_attr = inject(Data, annotation='new')

    instance = Injector(Module()).get_instance(Child)

    def parent_attribute_should_be_set():
        assert isinstance(instance.parent_attr, OldData)

    def child_attribute_should_be_set():
        assert isinstance(instance.child_attr, NewData)


def describe_inheriting_a_method():
    class Parent(object):
        @inject(value=Data, annotation='old')
        def set_parent_value(self, value):
            self.parent_value = value

    class Child(Parent):
        @inject(value=Data, annotation='new')
        def set_child_value(self, value):
            self.child_value = value

    instance = Injector(Module()).get_instance(Child)

    def parent_value_should_be_set():
        assert isinstance(instance.parent_value, OldData)

    def child_value_should_be_set():
        assert isinstance(instance.child_value, NewData)


def describe_overriding_an_inherited_method():
    class Parent(object):
        @inject(value=Data, annotation='old')
        def set_value(self, value):
            self.value = value

    class Child(Parent):
        @inject(value=Data, annotation='new')
        def set_value(self, value):
            self.value = value

    instance = Injector(Module()).get_instance(Child)

    def value_should_be_set_by_child():
        assert isinstance(instance.value, NewData)

