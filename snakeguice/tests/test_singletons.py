#!/usr/bin/env python

"""
Tests for the singleton scope.py
"""

from snakeguice import inject, Injected
from snakeguice import Injector

import cls_heirarchy as ch


class TestSingletonScope(object):

    class DomainObject(object):
        logger_a = inject(ch.Logger)
        logger_b = inject(ch.Logger)
        logger_c = inject(ch.Logger)
        place_a = inject(ch.Place, annotation='hot')
        place_b = inject(ch.Place, annotation='hot')
        place_c = inject(ch.Place, annotation='cold')
        place_d = inject(ch.Place, annotation='cold')

    def assert_obj(self, obj):
        assert obj.logger_a is obj.logger_b
        assert obj.logger_b is obj.logger_c
        assert obj.place_a is obj.place_b
        assert obj.place_c is obj.place_d
        assert obj.place_a is not obj.place_d

    def test_to_instance(self):
        class MyModule:
            def configure(self, binder):
                binder.bind(ch.Logger, to_instance=ch.ConcreteLogger())
                binder.bind(ch.Place, annotated_with='hot',
                        to_instance=ch.Beach())
                binder.bind(ch.Place, annotated_with='cold',
                        to_instance=ch.Glacier())

        obj = Injector(MyModule()).get_instance(self.DomainObject)
        self.assert_obj(obj)

    def test_eager_singleton(self):
        class MyModule:
            def configure(self, binder):
                binder.bind(ch.Logger, to_eager_singleton=ch.ConcreteLogger)
                binder.bind(ch.Place, annotated_with='hot',
                        to_eager_singleton=ch.Beach)
                binder.bind(ch.Place, annotated_with='cold',
                        to_eager_singleton=ch.Glacier)

        obj = Injector(MyModule()).get_instance(self.DomainObject)
        self.assert_obj(obj)

    def test_lazy_singleton(self):
        class MyModule:
            def configure(self, binder):
                binder.bind(ch.Logger, to_lazy_singleton=ch.ConcreteLogger)
                binder.bind(ch.Place, annotated_with='hot',
                        to_lazy_singleton=ch.Beach)
                binder.bind(ch.Place, annotated_with='cold',
                        to_lazy_singleton=ch.Glacier)

        obj = Injector(MyModule()).get_instance(self.DomainObject)
        self.assert_obj(obj)

    def _test_inject_into_eager_singleton(self):
        class MyLogger(object):
            hot_place = inject(ch.Place, annotation='hot')
            cold_place = inject(ch.Place, annotation='cold')

        class MyModule:
            def configure(self, binder):
                binder.bind(ch.Logger, to_eager_singleton=MyLogger)
                binder.bind(ch.Place, annotated_with='hot',
                        to_eager_singleton=ch.Beach)
                binder.bind(ch.Place, annotated_with='cold',
                        to_eager_singleton=ch.Glacier)

        obj = Injector(MyModule()).get_instance(self.DomainObject)
        self.assert_obj(obj)
        assert obj.logger_a.hot_place is obj.place_a
        assert obj.logger_a.cold_place is obj.place_c

    def _test_inject_into_lazy_singleton(self):
        class MyLogger(object):
            hot_place = inject(ch.Place, annotation='hot')
            cold_place = inject(ch.Place, annotation='cold')

        class MyModule:
            def configure(self, binder):
                binder.bind(ch.Logger, to_lazy_singleton=MyLogger)
                binder.bind(ch.Place, annotated_with='hot',
                        to_lazy_singleton=ch.Beach)
                binder.bind(ch.Place, annotated_with='cold',
                        to_lazy_singleton=ch.Glacier)

        obj = Injector(MyModule()).get_instance(self.DomainObject)
        self.assert_obj(obj)
        assert obj.logger_a.hot_place is obj.place_a
        assert obj.logger_a.cold_place is obj.place_c
