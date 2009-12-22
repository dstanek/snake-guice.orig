from os import path
from snakeguice.extras.snakeweb import RoutesModule

from controllers import HomeController


class MainModule(object):

    def configure(self, binder):
        app_dir = path.dirname(__file__)
        binder.bind(str, annotated_with='base template directory',
                    to_instance=app_dir)


class URLMapperModule(RoutesModule):

    def configure_mapper(self, mapper):
        mapper.connect('/form', controller=HomeController, action='form',
                      conditions=dict(method='POST'))
        mapper.connect('/', controller=HomeController, action='index')
