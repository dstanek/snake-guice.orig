#!/usr/bin/env python

import nose
import pymock
import mocker
from unittest import TestCase

import snakeguice as sg

#
# sample class heirarchy
#

class Person(object):
    pass

class GoodPerson(Person):
    x = 'good'

class EvilPerson(Person):
    x = 'evil'


#
# tests for the Binder class
#

class _TestBinder(TestCase):
    """Tests for the Binder class."""

    def setUp(self):
        self.binder = sg.Binder()

    def test_add_error(self):
        """Test the accumulation of errors in the Binder class."""
        binder = self.binder
        binder.add_error(Exception, 'just a basic exception')
        binder.add_error(NotImplementedError, "this thing isn't implemented")
        assert len(binder._errors) == 2
        assert isinstance(binder._errors[0], Exception)
        assert isinstance(binder._errors[1], NotImplementedError)

    def test_bind(self):
        binding = self.binder.bind(Person)
        assert isinstance(binding, sg.Binding)
        assert Person in self.binder._map

    @nose.tools.raises(sg.BindingError)
    def test_duplicate_keys(self):
        self.binder.bind(Person)
        self.binder.bind(Person) # this should fail

    def test_get_binding(self):
        self.binder.bind(Person)
        binding = self.binder.get_binding(Person)
        assert isinstance(binding, sg.Binding)


class _TestBinding(TestCase):
    """Test the Binding class."""

    def setUp(self):
        self.binding = sg.Binding(Person)

    def check_keys(self, *keys):
        for key in keys:
            assert key in self.binding._keys

    def test_binding(self):
        assert self.binding._baseclass is Person

    def test_to(self):
        rv = self.binding.to(EvilPerson)
        assert rv is self.binding

    def test_toProvider(self):
        rv = self.binding.to_provider(object())
        assert rv is self.binding

    def test_bind_to_oneself(self):
        """Not binding to anything implicitly binds to oneself."""
        binding = sg.Binding(EvilPerson)
        assert binding.get_implementation() is EvilPerson

    #def test_bind_properties(self):
    #    binding = sg.Binding(Person)
    #    binding.bind_property(Person.name, str)

    #def test_and_to(self):
    #    rv = self.binding.to('otherkey')
    #    assert rv is self.binding
    #    self.check_keys('otherkey', 'somekey')

    #@nose.tools.raises(sg.BindingError)
    #def test_duplicate_keys(self):
    #    self.binding.to('x').and_to('x')


def _test_binding_classes_to_strings():
    binder = sg.Binder()
    binder.bind(GoodPerson).to('good')
    binder.bind(EvilPerson).to('evil')
