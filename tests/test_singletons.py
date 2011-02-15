#!/usr/bin/env python

"""
Tests for the singleton scope.py
"""

from snakeguice import inject, scopes, Injector, annotate

import cls_heirarchy as ch


class TestSingletonScope(object):

    class DomainObject(object):

        @inject(logger_a=ch.Logger, logger_b=ch.Logger, logger_c=ch.Logger)
        def set_loggers(self, logger_a, logger_b, logger_c):
            self.logger_a = logger_a
            self.logger_b = logger_b
            self.logger_c = logger_c

        @inject(place_a=ch.Place)
        @annotate(place_a='hot')
        def set_place_a(self, place_a):
            self.place_a = place_a

        @inject(place_b=ch.Place)
        @annotate(place_b='hot')
        def set_place_b(self, place_b):
            self.place_b = place_b

        @inject(place_c=ch.Place)
        @annotate(place_c='cold')
        def set_place_c(self, place_c):
            self.place_c = place_c

        @inject(place_d=ch.Place)
        @annotate(place_d='cold')
        def set_place_d(self, place_d):
            self.place_d = place_d

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

    def _test_inject_into_singleton(self):
        class MyLogger(object):
            hot_place = inject(ch.Place, annotation='hot')
            cold_place = inject(ch.Place, annotation='cold')

        class MyModule:
            def configure(self, binder):
                binder.bind(ch.Logger, to=MyLogger, in_scope=scopes.SINGLETON)
                binder.bind(ch.Place, annotated_with='hot',
                            to=ch.Beach, to_scope=scopes.SINGLETON)
                binder.bind(ch.Place, annotated_with='cold',
                            to=ch.Glacier, to_scope=scopes.SINGLETON)

        obj = Injector(MyModule()).get_instance(self.DomainObject)
        self.assert_obj(obj)
        assert obj.logger_a.hot_place is obj.place_a
        assert obj.logger_a.cold_place is obj.place_c
