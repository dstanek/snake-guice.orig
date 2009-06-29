#!/usr/bin/env python

import routes


class RoutesBinder(object):

    def __init__(self, mapper, annotation):
        self.mapper = mapper
        self._annotation = annotation
        self.controller_map = {}

    def connect(self, *args, **kwargs):

        controller = kwargs.get('controller')

        if controller is None:
            raise TypeError('no controller specified')
        
        if not isinstance(controller, type):
            raise TypeError('controller must be a class')

        key = unicode(str(controller))
        self.controller_map[key] = controller
        kwargs['controller'] = key
        self.mapper.connect(*args, **kwargs)


class RoutesModule(object):

    annotation = None

    def configure(self, binder):
        self._mapper = routes.Mapper()
        self.routes_binder = RoutesBinder(self._mapper, self.annotation)
        binder.bind(RoutesBinder,
                         to_instance=self.routes_binder,
                         annotated_with=self.annotation)
        self.configure_mapper(self.routes_binder)
        self._mapper.create_regs([])

    def configure_mapper(self, mapper):
        raise NotImplementedError(
                'you must provide a configure_mapper implementation')


class Application(object):

    def __init__(self, injector):
        self._injector = injector

    def __call__(self, environ, start_response):
        from webob import Request
        request = Request(environ)

        binder = self._injector.get_instance(RoutesBinder)

        # TODO: i have a patch that makes this suck less - i need to submit it
        binder.mapper.environ = environ

        route = binder.mapper.match(environ['PATH_INFO'])
        if not route:
            return webob.exc.HTTPNotFound

        controller = route.pop('controller')
        controller = binder.controller_map.get(controller)
        if not controller:
            return webob.exc.HTTPNotFound

        controller = self._injector.get_instance(controller)
        try:
            action = route.pop('action')
        except KeyError:
            action = 'index'

        if not hasattr(controller, action):
            return webob.exc.HTTPNotFound

        action = getattr(controller, action)
        print action, request

        response = action(request, **route)
        return response(environ, start_response)
