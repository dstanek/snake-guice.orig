#!/usr/bin/env python

"""Tests for the assisted injection feature."""

from nose.tools import raises

from snakeguice import inject, create_injector, annotate
from snakeguice.assist import assisted_inject, assisted, AssistProvider
from snakeguice.errors import AssistError


class IService(object):
    """An interface for services."""


class IWorkerFactory(object):
    """An interface to create Worker instances."""


class CustomerService(object):
    """A concrete service for dealing with customers."""


class OrderService(object):
    """A concrete service for dealing with orders."""


class Worker(object):
    """Uses services to do real work."""

    @assisted_inject(c_service=CustomerService, o_service=OrderService)
    @annotate(c_service="customer", o_service="order")
    def __init__(self, c_service, o_service, name, date):
        self.c_service = c_service
        self.o_service = o_service
        self.name = name
        self.date = date


class Manager(object):
    """Makes sure that the worker does its work."""

    @inject(worker_factory=IWorkerFactory)
    def __init__(self, worker_factory):
        self.worker = worker_factory.create(name='awesome worker',
                                            date='07/09/2010')


class Module(object):

    def configure(self, binder):
        binder.bind(IWorkerFactory, to_provider=AssistProvider(Worker))
        binder.bind(IService, annotated_with="customer", to=CustomerService)
        binder.bind(IService, annotated_with="order", to=OrderService)


class test_partiall_injecting_an_object(object):

    def setup(self):
        inj = create_injector([Module()])
        self.manager = inj.get_instance(Manager)

    def test(self):
        assert isinstance(self.manager.worker, Worker)


class base_AssistProvider_decorator_errors(object):

    @raises(AssistError)
    def test_that_an_exception_is_raised(self):
        AssistProvider(self.C)


class test_creating_an_AssistProvider_from_an_inject(
        base_AssistProvider_decorator_errors):

    def setup(self):
        class C(object):
            @inject(x=object)
            def __init__(self, x):
                pass
        self.C = C


class test_creating_an_AssistProvider_from_an_uninjected_object(
        base_AssistProvider_decorator_errors):

    def setup(self):
        class C(object):
            pass
        self.C = C


@raises(AssistError)
def test_using_assisted_inject_on_a_method():

    class C(object):

        @assisted_inject(x=object)
        def m(self, x):
            pass
