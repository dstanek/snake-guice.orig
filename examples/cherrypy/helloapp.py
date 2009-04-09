import cherrypy
from snakeguice import Injector

from controller import HelloWorld
from providers import UserProvider, RequestDataProvider
from scopes import CHERRYPY_REQUEST_SCOPE, CHERRYPY_SESSION_SCOPE


class Module(object):

    def configure(self, binder):
        binder.bind(UserProvider, to=UserProvider,
                in_scope=CHERRYPY_SESSION_SCOPE)
        binder.bind(RequestDataProvider, to=RequestDataProvider,
                in_scope=CHERRYPY_REQUEST_SCOPE)


injector = Injector(Module())
controller = injector.get_instance(HelloWorld)
cherrypy.quickstart(controller, '/', 'config.ini')
