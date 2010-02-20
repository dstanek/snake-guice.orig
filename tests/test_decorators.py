"""Behavioral tests for the snake-guice decorators."""

from nose.tools import raises

from snakeguice.decorators import inject, GuiceArg, annotate
from snakeguice.decorators import provide, Provided


def test_inject_init():
    """Using the inject decorator on a constructor."""

    class SomeClass(object):

        @inject(x=int)
        def __init__(self, x):
            pass

    assert SomeClass.__guice__.init == {'x': GuiceArg(int)}
    assert len(SomeClass.__guice__.methods) == 0


def test_inject_methods():
    """Using the inject decorator on a method."""

    class SomeClass(object):

        @inject(y=float)
        def go(self, y):
            pass

    assert SomeClass.__guice__.init is None
    assert SomeClass.__guice__.methods.items() == [
            ('go', {'y': GuiceArg(float)}),
    ]

def test_inject_all():
    """Using combinations of inject including annotations."""
    #TODO: add annotation stuff again

    class SomeClass(object):

        @inject(a=bool, b=int, c=float)
        @annotate(a='free', b='paid')
        def __init__(self, a, b, c):
            pass

        @inject(y=float)
        def go(self, y):
            pass

        @inject(x=int, y=int, z=object)
        @annotate(y='old', z='new')
        def stop(self, x, y, z):
            pass

    assert (SomeClass.__guice__.init ==
            {'a': GuiceArg(bool, 'free'),
             'b': GuiceArg(int, 'paid'),
             'c': GuiceArg(float)})
    print SomeClass.__guice__.methods.items()
    assert SomeClass.__guice__.methods.items() == [
            ('go', {'y': GuiceArg(float)}),
            ('stop',
             {'x': GuiceArg(int),
              'y': GuiceArg(int, 'old'),
              'z': GuiceArg(object, 'new')})]


@raises(TypeError)
def test_incorrect_methods0():
    """Ensure inject is validating method calls."""

    class SomeClass(object):

        @inject(int, y=int)
        def f(self, x, y):
            pass


@raises(TypeError)
def test_incorrect_methods1():
    """Ensure inject is validating method calls."""

    class SomeClass(object):

        @inject(z=int, y=int)
        def f(self, x, y):
            pass


@raises(TypeError)
def test_incorrect_methods2():
    """Ensure inject is validating method calls."""

    class SomeClass(object):

        @inject(y=int)
        def f(self, x, y):
            pass


@raises(TypeError)
def test_incorrect_methods3():
    """Ensure inject is validating method calls."""

    class SomeClass(object):

        @inject
        def f(self, x, y):
            pass


@raises(Exception)
def test_order_of_annotate():
    """The annotate decorator must me applied to a method before inject."""

    class SomeClass(object):

        @annotate(a='large')
        @inject(a=int)
        def f(self, a):
            pass
