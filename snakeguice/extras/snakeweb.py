#!/usr/bin/env python

from webob import Request, Response
from webob.exc import HTTPNotFound
import routes


class RoutesBinder(object):

    def __init__(self, mapper, annotation):
        self.mapper = mapper
        self._annotation = annotation
        self.controller_map = {}

    def connect(self, *args, **kwargs):

        controller = kwargs.get('controller')

        if controller is None:
            raise TypeError('No controller specified')

        if not isinstance(controller, type):
            raise TypeError('Controller must be a class')

        key = unicode(str(controller))
        self.controller_map[key] = controller
        kwargs['controller'] = key
        self.mapper.connect(*args, **kwargs)

    def match(self, url, environ):
        # TODO: i have a patch that makes this suck less - i need to submit it
        old_environ, self.mapper.environ = self.mapper.environ, environ
        try:
            return self.mapper.match(url)
        finally:
            self.mapper.environ = old_environ


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
        request = Request(environ)

        binder = self._injector.get_instance(RoutesBinder)

        route = binder.match(environ['PATH_INFO'], environ)
        if not route:
            return HTTPNotFound('No matching route')(environ, start_response)

        controller = route.pop('controller')
        controller = binder.controller_map.get(controller)
        if not controller:
            return HTTPNotFound()(environ, start_response)

        controller = self._injector.get_instance(controller)

        action = route.pop('action', 'index')
        action = getattr(controller, action, None)

        if not action and callable(controller):
            action = controller

        if not action:
            return HTTPNotFound()(environ, start_response)

        response = action(request, **route)
        return response(environ, start_response)
