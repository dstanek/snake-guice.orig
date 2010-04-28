import sys
import inspect


class GuiceData(object):

    def __init__(self):
        self.init = None
        self.methods = {}

    @classmethod
    def from_class(cls, target_class):
        if '__guice__' not in target_class.__dict__:
            guice_data = cls()
            try:
                target_class.__guice__ = guice_data
            except TypeError: # special case for builtin/extension types
                return guice_data
        return target_class.__guice__

    @classmethod
    def composite_from_class(cls, target_class):
        composite_data = GuiceData()
        for _cls in target_class.__mro__[-1::-1]:
            data = GuiceData.from_class(_cls)
            if data.init: # only the last class in the chain
                composite_data.init = data.init
            for name, method in data.methods.items():
                composite_data.methods[name] = method

        return composite_data

    @classmethod
    def from_class_dict(cls, class_dict):
        if '__guice__' not in class_dict:
            class_dict['__guice__'] = cls()
        return class_dict['__guice__']


class GuiceArg(object):

    def __init__(self, datatype=None, annotation=None, scope=None):
        self.datatype = datatype
        self.annotation = annotation
        self.scope = scope

    def __eq__(self, other):
        return (self.datatype, self.annotation, self.scope
                ) == (other.datatype, other.annotation, other.scope)


def _validate_func_args(func, kwargs):
    """Validate decorator args when used to decorate a function."""

    args, varargs, varkw, defaults = inspect.getargspec(func)
    if set(kwargs.keys()) != set(args[1:]): # chop off self
        raise TypeError("decorator kwargs do not match %s()'s kwargs"
                        % func.__name__)


def enclosing_frame(frame=None, level=2):
    """Get an enclosing frame that skips decorator code"""
    frame = frame or sys._getframe(level)
    while frame.f_globals.get('__name__') == __name__: frame = frame.f_back
    return frame


def inject(**kwargs):

    scope = kwargs.get('scope')
    if 'scope' in kwargs:
        del kwargs['scope']

    def _inject(func):
        class_locals = enclosing_frame().f_locals

        guice_data = GuiceData.from_class_dict(class_locals)

        annotations = getattr(func, '__guice_annotations__', {})

        gmethod = dict((k, GuiceArg(v, annotations.get(k)))
                       for k, v in kwargs.items())

        if func.__name__ == '__init__':
            _validate_func_args(func, kwargs)
            guice_data.init = gmethod
        else:
            _validate_func_args(func, kwargs)
            guice_data.methods[func.__name__] = gmethod

        return func

    return _inject


class annotate(object):

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, method):
        class_locals = enclosing_frame().f_locals
        if '__guice__' in class_locals:
            if method.__name__ in class_locals['__guice__'].methods:
                raise Exception('annotate must be applied before inject')
        method.__guice_annotations__ = self.kwargs
        return method


class provides(object):

    def __init__(self, type):
        self._type = type

    def __call__(self, method):
        method.__guice_provides__ = self._type
        return method
