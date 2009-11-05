#!/usr/bin/env python

"""
Examples of using the snakeguice API.
"""

#TODO: add a test proving call throughs work


from snakeguice import inject, Injected, ParameterInterceptor, annotate
from snakeguice import Injector

import cls_heirarchy as ch


def test_default_binding():
    """Not binding to anything implicitly binds to oneself."""
    injector = Injector([])
    person = injector.get_instance(ch.Person)
    assert isinstance(person, ch.Person)


def test_injector_simple():
    class MyModule:
        def configure(self, binder):
            binder.bind(ch.Person, to=ch.EvilPerson)

    injector = Injector(MyModule())
    person = injector.get_instance(ch.Person)
    assert isinstance(person, ch.EvilPerson)


def __test_annotated_injector():
    class DomainObject(object):
        @inject(person0=ch.Person, annotation='good')
        @inject(person1=ch.Person, annotation='evil')
        @inject(person2=ch.Person)
        def __init__(self, person0=Injected, person1=Injected,
                person2=Injected):
            self.person0 = person0
            self.person1 = person1
            self.person2 = person2

    class MyModule:
        def configure(self, binder):
            binder.bind(DomainObject, to=DomainObject)
            binder.bind(ch.Person, annotated_with='evil', to=ch.EvilPerson)
            binder.bind(ch.Person, annotated_with='good', to=ch.GoodPerson)

    injector = Injector(MyModule())
    obj = injector.get_instance(DomainObject)
    assert isinstance(obj.person0, ch.GoodPerson)
    assert isinstance(obj.person1, ch.EvilPerson)
    assert isinstance(obj.person2, ch.Person)


def test_annotations():
    class DomainObject(object):
        @inject(hero=ch.Person, villian=ch.Person, victim=ch.Person)
        @annotate(hero='good', villian='evil')
        def __init__(self, hero=Injected, villian=Injected, victim=Injected):
            self.hero = hero
            self.villian = villian
            self.victim = victim

    class ByStander(ch.Person):
        pass

    class MyModule:
        def configure(self, binder):
            binder.bind(ch.Person, annotated_with='evil', to=ch.EvilPerson)
            binder.bind(ch.Person, annotated_with='good', to=ch.GoodPerson)
            binder.bind(ch.Person, to=ByStander)

    injector = Injector(MyModule())
    obj = injector.get_instance(DomainObject)
    assert isinstance(obj.hero, ch.GoodPerson)
    assert isinstance(obj.villian, ch.EvilPerson)
    assert isinstance(obj.victim, ByStander)


def test_injector_injecting_a_provider():

    class SimpleProvider(object):
        def get(self):
            return ch.GoodPerson()

    class MyModule:
        def configure(self, binder):
            binder.bind(ch.Person, to=SimpleProvider)

    injector = Injector(MyModule())
    person_provider = injector.get_instance(ch.Person)
    assert isinstance(person_provider.get(), ch.GoodPerson)


def test_injector_injecting_from_a_provider():

    class SimpleProvider(object):
        def get(self):
            return ch.GoodPerson()

    class MyModule:
        def configure(self, binder):
            binder.bind(ch.Person, to_provider=SimpleProvider)

    injector = Injector(MyModule())
    person = injector.get_instance(ch.Person)
    assert isinstance(person, ch.GoodPerson)


def Xtest_collision():
    """TODO: figure out what to do with this"""


def test_inject_provider_with_args():

    class PersonProvider(object):
        def get(self, typ):
            if typ == 'good':
                return ch.GoodPerson
            elif typ == 'evil':
                return ch.EvilPerson
            else:
                return None

    class MyModule:
        def configure(self, binder):
            binder.bind(ch.Person, to=PersonProvider)

    injector = Injector(MyModule())
    person_provider = injector.get_instance(ch.Person)
    assert person_provider.get('good') == ch.GoodPerson
    assert person_provider.get('evil') == ch.EvilPerson
    assert person_provider.get('clueless') is None


def test_inject_decorator():

    class DomainObject(object):

        @inject(logger=ch.Logger)
        def __init__(self, logger=Injected):
            assert isinstance(logger, ch.ConcreteLogger)

        @inject(person=ch.Person)
        def do_something(self, person=Injected):
            assert isinstance(person, ch.EvilPerson)

        @inject(person=ch.Person, logger=ch.Logger)
        def multipl(self, logger=Injected, person=Injected):
            assert isinstance(person, ch.EvilPerson)
            assert isinstance(logger, ch.ConcreteLogger)

    class MyModule:
        def configure(self, binder):
            binder.bind(ch.Person, to=ch.EvilPerson)
            binder.bind(ch.Logger, to=ch.ConcreteLogger)

    injector = Injector(MyModule())
    o = injector.get_instance(DomainObject)
        

class TestMethodInterceptors(object):

    def setup(self):
        class MyModule:
            def configure(self, binder):
                binder.bind(ch.Person, to=ch.EvilPerson)
                binder.bind(ch.Logger, to_instance=ch.ConcreteLogger())
                binder.bind(ch.Person, annotated_with='good', to=ch.GoodPerson)
                binder.bind(ch.Person, annotated_with='evil', to=ch.EvilPerson)

        self.injector = Injector(MyModule())
        self.interceptor = ParameterInterceptor(self.injector)

    def test_noargs(self):
        class DomainObject(object):
            @self.interceptor(person=ch.Person, annotation='evil')
            def intercept_me(self, person=Injected):
                assert isinstance(person, ch.EvilPerson)

        obj = self.injector.get_instance(DomainObject)
        obj.intercept_me()

    def test_args(self):
        class DomainObject(object):
            @self.interceptor(person=ch.Person, annotation='evil')
            def intercept_me(self, arg0,
                    kwarg0=None, kwarg1=None, person=Injected):
                assert arg0 == 0
                assert kwarg0 == 1
                assert kwarg1 is None
                assert isinstance(person, ch.EvilPerson)

        obj = self.injector.get_instance(DomainObject)
        obj.intercept_me(0, kwarg0=1)

    def test_stacking(self):
        class DomainObject(object):
            @self.interceptor(person0=ch.Person, annotation='good')
            @self.interceptor(person1=ch.Person, annotation='evil')
            def intercept_me(self, person0=Injected, person1=Injected):
                assert isinstance(person0, ch.GoodPerson)
                assert isinstance(person1, ch.EvilPerson)

        obj = self.injector.get_instance(DomainObject)
        obj.intercept_me()

#TODO: constant injection

#TODO: provider injection
