#!/usr/bin/env python

"""
injector module unit tests
"""

from dingus import Dingus

from snakeguice import create_injector, injector, binder
import cls_heirarchy as ch


class FakeModule(object):

    def __init__(self):
        self.binder = None
        self.num_calls = 0

    def configure(self, binder):
        self.binder = binder
        self.num_calls +=1

    def was_called(self):
        return self.num_calls


def test_injector_single_module_init():
    """Create an Injector that accepts a single Module instance."""

    module = FakeModule()
    inj = injector.Injector(module)
    assert isinstance(inj, injector.Injector)
    assert isinstance(module.binder, binder.Binder)


def test_injector_multi_module_init():
    """Create an Injector that accepts any number of Module instances."""

    modules = [FakeModule(), FakeModule(), FakeModule()]
    inj = injector.Injector(modules)
    assert isinstance(inj, injector.Injector)
    for module in modules:
        assert isinstance(module.binder, binder.Binder)


def test_create_child():
    """Create an injector child."""
    class ParentModule:
        def configure(self, binder):
            binder.bind(ch.Person, to=ch.EvilPerson)

    class ChildModule:
        def configure(self, binder):
            binder.bind(ch.Person, annotated_with='good', to=ch.GoodPerson)

    inj = injector.Injector(ParentModule())
    person = inj.get_instance(ch.Person)
    assert isinstance(person, ch.EvilPerson)

    child_inj = inj.create_child(ChildModule())
    person = child_inj.get_instance(ch.Person)
    assert isinstance(person, ch.EvilPerson)
    person = child_inj.get_instance(ch.Person, 'good')
    assert isinstance(person, ch.GoodPerson)


class test_using_create_injector_factory(object):

    def setup(self):
        class PeopleModule(object):
            def configure(self, binder):
                binder.bind(ch.Person, to=ch.EvilPerson)
        self.injector = create_injector([PeopleModule()])
        self.instance = self.injector.get_instance(ch.Person)

    def test_an_injector_was_returned(self):
        assert isinstance(self.injector, injector.Injector)

    def test_correct_instance_was_created(self):
        assert isinstance(self.instance, ch.EvilPerson)


def test_create_an_injector_without_any_modules():
    modules = [FakeModule(), FakeModule(), FakeModule()]


class test_using_get_provider(object):

    def setup(self):
        class PeopleModule(object):
            def configure(self, binder):
                binder.bind(ch.Person, to=ch.EvilPerson)
        self.injector = create_injector([PeopleModule()])
        self.provider = self.injector.get_provider(ch.Person)
        self.instance = self.provider.get()

    def test_provider_provides_an_instance(self):
        assert isinstance(self.instance, ch.EvilPerson)
