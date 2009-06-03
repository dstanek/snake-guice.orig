from nose.tools import raises
from snakeguice.errors import DecorationError
from snakeguice.decorators import inject, GuiceProperty, GuiceMethod
from snakeguice.decorators import provide, Provided


def test_inject_init():
    """Using the inject decorator on a constructor."""

    class SomeClass(object):
    
        @inject(x=int)
        def __init__(self, x):
            pass
    
    assert SomeClass.__guice__.init == GuiceMethod({'x': int})
    assert len(SomeClass.__guice__.methods) == 0
    assert len(SomeClass.__guice__.properties) == 0


def test_inject_methods():
    """Using the inject decorator on a method."""

    class SomeClass(object):
    
        @inject(y=float)
        def go(self, y):
            pass

    assert SomeClass.__guice__.init is None
    assert SomeClass.__guice__.methods.items() == [
            ('go', GuiceMethod({'y': float})),
    ]
    assert len(SomeClass.__guice__.properties) == 0

def test_inject_provider():
    """ Using property injection, and then auto-providing instance to
        a method.
    """
    from snakeguice import injector
    from snakeguice.providers import InstanceProvider

    # we want a specific instance of Something to be provided to a method
    # in SomeClass
    class Something(object):
        def __init__(self, status):
            self.status = status

    # SomeClass has an injected provider property, and a method that expects
    # the provided instance as an attribute to its method
    class SomeClass(object):
        some_provider = inject(InstanceProvider)

        @provide(p=some_provider)
        def get_some_status(self, p):
            assert type(p) == Something
            assert p.status == 'something:provided'
            return p.status

    class Modules:
        def configure(self, binder):
            provided = InstanceProvider(Something('something:provided'))
            binder.bind(InstanceProvider, to_instance=provided)

    inj = injector.Injector(Modules())
    some_class = inj.get_instance(SomeClass)
    assert isinstance(some_class, SomeClass)
    
    status = some_class.get_some_status()
    assert status == 'something:provided'

def test_inject_properties():
    """Using the inject decorator on a property."""

    class SomeClass(object):
        prop_a = inject(int)
        prop_b = inject(object)

    assert SomeClass.__guice__.init is None
    assert len(SomeClass.__guice__.methods) == 0
    assert SomeClass.__guice__.properties.items() == [
            ('prop_a', GuiceProperty(int)),
            ('prop_b', GuiceProperty(object)),
    ]


def test_inject_all():
    """Using combinations of inject including annotations."""

    class SomeClass(object):
        prop_a = inject(int)
        prop_b = inject(object, annotation='test')
    
        @inject(a=bool, b=int, c=float, annotation='test')
        def __init__(self, a, b, c):
            pass
    
        @inject(y=float)
        def go(self, y):
            pass

        @inject(x=int, y=int, z=object, annotation='test')
        def stop(self, x, y, z):
            pass

    assert (SomeClass.__guice__.init ==
            GuiceMethod({'a': bool, 'b': int, 'c': float}, 'test'))
    assert SomeClass.__guice__.methods.items() == [
            ('go', GuiceMethod({'y': float})),
            ('stop', GuiceMethod({'x': int, 'y': int, 'z': object}, 'test')),
    ]
    assert SomeClass.__guice__.properties.items() == [
            ('prop_a', GuiceProperty(int)),
            ('prop_b', GuiceProperty(object, 'test')),
    ]


@raises(DecorationError)
def test_incorrect_methods0():
    """Ensure inject is validating method calls."""

    class SomeClass(object):
        
        @inject(int, y=int)
        def f(self, x, y):
            pass

@raises(DecorationError)
def test_incorrect_methods1():
    """Ensure inject is validating method calls."""

    class SomeClass(object):
        
        @inject(z=int, y=int)
        def f(self, x, y):
            pass

@raises(DecorationError)
def test_incorrect_methods1():
    """Ensure inject is validating method calls."""

    class SomeClass(object):
        
        @inject(y=int)
        def f(self, x, y):
            pass

#@raises(DecorationError)
# TODO: make a test case for a bare inject
#def test_incorrect_methods2():
#    """Ensure inject is validating method calls."""
#
#    class SomeClass(object):
#        
#        @inject
#        def f(self, x, y):
#            pass

@raises(DecorationError)
def test_incorrect_properties0():
    """Ensure inject is validating property calls."""

    class SomeClass(object):
        prop_a = inject(prop_a=int)
        prop_b = inject(object)


@raises(DecorationError)
def test_incorrect_properties1():
    """Ensure inject is validating property calls."""

    class SomeClass(object):
        prop_a = inject(int, prop_a=int)
        prop_b = inject(object)
