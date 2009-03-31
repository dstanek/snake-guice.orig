#!python


from peak.util.decorators import decorate_assignment


class ParameterInterceptor(object):

    def __init__(self, injector):
        self._injector = injector

    def __call__(self, annotation=None, **kwargs):
        #TODO: add a test for more than one kwargs
        (param_name, param_type) = kwargs.items()[0]

        def callback(frame, name, func, old_locals):
            def _f(*args, **kwargs): # it is OK to override the outer function
                kwargs[param_name] = self._injector.get_instance(
                        param_type, annotation)
                return func(*args, **kwargs)
            return _f

        return decorate_assignment(callback)
