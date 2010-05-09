"""A really simple 'Hello, World' webapp to test snakeweb."""

from wsgiref.simple_server import make_server
from snakeguice import create_injector
from snakeguice.modules import Module
from snakeguice.extras import snakeweb


class HWController(object):

    def index(self, request):
        return snakeweb.Response('Hello, World!<br>I see you are from: {0}'
                                 .format(request.remote_addr))

    def hello_name(self, request, name):
        return snakeweb.Response('Hello, {0}!'.format(name))


class HWModule(Module):

    def configure(self, binder):
        self.install(binder, HWRoutes())


class HWRoutes(snakeweb.RoutesModule):

    def configure(self, routes_binder):
        routes_binder.connect('/', controller=HWController)
        routes_binder.connect('/:name', controller=HWController,
                              action='hello_name')


if __name__ == '__main__':
    injector = create_injector(HWModule())
    httpd = make_server('', 8000, snakeweb.Application(injector))
    httpd.serve_forever()
