import sys
import inspect

from snakeguice.odict import OrderedDict
from snakeguice.errors import DecorationError


class GuiceData(object):

    def __init__(self):
        self.init = None
        self.methods = OrderedDict()


class GuiceArg(object):

    def __init__(self, datatype=None, annotation=None):
        self.datatype = datatype
        self.annotation = annotation

    def __eq__(self, other):
        return (self.datatype, self.annotation
                ) == (other.datatype, other.annotation)


class Provided(object):
    """ Interface for argument to be provided. """


def _validate_func_args(func, args, kwargs):
    """Validate decorator args when used to decorate a function."""
    if args:
        raise DecorationError('args cannot be passed into the decorator')

    args, varargs, varkw, defaults = inspect.getargspec(func)
    if set(kwargs.keys()) != set(args[1:]): # chop off self
        raise DecorationError('the kwargs passed into the docorator do '
                'not match the decorated function')


def _validate_property_args(func, args, kwargs): # pylint: disable-msg=W0613
    """Validate decorator args when used with a class attribute."""
    if len(args) != 1:
        raise DecorationError('only 1 decorator argument allowed')
    if kwargs:
        raise DecorationError('keyword args cannot be specified '
                'when decorating a property')


def enclosing_frame(frame=None, level=2):
    """Get an enclosing frame that skips decorator code"""
    frame = frame or sys._getframe(level)
    while frame.f_globals.get('__name__')==__name__: frame = frame.f_back
    return frame


def inject(*args, **kwargs):

    annotation = kwargs.get('annotation')
    if 'annotation' in kwargs:
        del kwargs['annotation']

    scope = kwargs.get('scope')
    if 'scope' in kwargs:
        del kwargs['scope']

    def _inject(func):
        class_locals = enclosing_frame().f_locals
        #if not hasattr(func, 'im_class'):
        #    raise DecorationError("snake-guice can't inject into functions")

        guice_data = class_locals.get('__guice__')
        if not guice_data:
            guice_data = class_locals['__guice__'] = GuiceData()

        annotations = getattr(func, '__guice_annotations__', {})

        gmethod = dict((k, GuiceArg(v, annotations.get(k)))
                       for k, v in kwargs.items())

        if func.__name__ == '__init__':
            _validate_func_args(func, args, kwargs)
            guice_data.init = gmethod
        else:
            _validate_func_args(func, args, kwargs)
            guice_data.methods[func.__name__] = gmethod
    
        return func

    return _inject


class provide(object):
    """ Decorator for method with arguments to be provided by DI at runtime.
        This differs from the snake-guice "inject" decorator, which creates
        dependencies at class-load time.  It assumes the provider has a
        get() method that is able to look up the contextually-accurate
        instance.
    """

    def __init__(self, **providers):
        """ Initialize a "provide" decorator with the given providers.  The
            argument name should map to an kwarg in the decorated method.  The
            argument value should map to an injected provider in the containing
            class.
            @param keyword list of providers
        """
        self.providers = providers

    def __call__(self, method):
        """ Wrap the method definition with the provisioner.
            @param method to be decorated
            @return decorated function
        """
        def decorated(cls, *args, **kwargs):
            for name, val in self.providers.items():
                # val.name is assumed to be given by the inject decorator.
                # we have to look it up in the class dictionary since we don't
                # get the injected version when the provide decorator is made
                kwargs[name] = getattr(cls, val.name).get()
            return method(cls, *args, **kwargs)

        decorated.__doc__ = method.__doc__
        return decorated


class annotate(object):

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, method):
        method.__guice_annotations__ = self.kwargs
        return method
