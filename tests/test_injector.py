#!/usr/bin/env python

"""
injector module unit tests
"""

import mocker

from snakeguice import injector, Injected
import cls_heirarchy as ch


def test_injector_single_module_init():
    """Create an Injector that accepts a single Module instance."""

    c = mocker.Mocker()
    mock_module = c.mock()
    mock_module.configure(mocker.ANY)

    c.replay()
    inj = injector.Injector(mock_module)
    c.verify()
    assert isinstance(inj, injector.Injector)


def test_injector_multi_module_init():
    """Create an Injector that accepts any number of Module instances."""

    c = mocker.Mocker()
    mock_module0 = c.mock()
    mock_module1 = c.mock()
    mock_module0.configure(mocker.ANY)
    mock_module1.configure(mocker.ANY)

    c.replay()
    inj = injector.Injector([mock_module0, mock_module1])
    c.verify()
    assert isinstance(inj, injector.Injector)


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
