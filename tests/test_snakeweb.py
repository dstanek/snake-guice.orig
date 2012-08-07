from nose.tools import raises
from nose.plugins.skip import SkipTest
from mock import Mock, patch

from snakeguice.extras import snakeweb


class TestRoutesModuleSetup(object):

    @patch('snakeguice.extras.snakeweb.routes')
    def setup(self, mock_routes):
        self.mock_routes = mock_routes

        class MyRoutesModule(snakeweb.RoutesModule):
            configure = Mock()

        self.binder = Mock()
        self.module = MyRoutesModule()
        self.module.run_configure(binder=self.binder)

    def test_configure_is_called_with_a_mapper(self):
        raise SkipTest
        assert self.module.configure.calls('()',
                snakeweb.RoutesBinder.return_value)

    def test_real_routes_mapper_was_created(self):
        assert self.mock_routes.Mapper.calls()


class TestRoutesModuleIsAbstract(object):

    def setup(self):
        self.module = snakeweb.RoutesModule()

    @raises(NotImplementedError)
    def test_configure_mapper_is_not_implemented(self):
        self.module.configure(Mock())


class BaseTestRoutesBinder(object):

    def setup(self):
        self.routes_mapper = Mock()
        self.annotation = Mock()
        self.binder = snakeweb.RoutesBinder(self.routes_mapper,
                                            self.annotation)


class TestRoutesBinderConnectWithInvalidControllers(BaseTestRoutesBinder):

    @raises(TypeError)
    def test_an_exception_is_raised_is_no_controller_is_specified(self):
        self.binder.connect('/post/3/view')


class TestWhenCallingRoutesBinder(BaseTestRoutesBinder):

    def setup(self):
        super(TestWhenCallingRoutesBinder, self).setup()
        self.controller = object
        self.args = (Mock(), Mock())
        self.kwargs = dict(a=Mock(), controller=object)
        self.binder.connect(*self.args, **self.kwargs)

        self.key = unicode((id(self.controller), repr(self.controller)))
        self.kwargs['controller'] = self.key

    def test_pass_through_to_real_mapper(self):
        assert self.routes_mapper.calls('connect', *self.args, **self.kwargs)

    def test_controller_should_be_added_to_the_map(self):
        assert self.binder.controller_map == {self.key: self.controller}


class TestWhenAutoConfiguringRoutes(object):

    @patch('snakeguice.extras.snakeweb.RoutesBinder')
    def setup(self, mock_RoutesBinder):

        class MyController(object):
            def __call__(self):
                pass

            def bar(self, request):
                pass

        self.controller = MyController

        class MyModule(snakeweb.AutoRoutesModule):
            configured_routes = {
                '/': MyController,
                '/foo': MyController.bar,
            }

        self.module = MyModule()
        self.module.run_configure(binder=Mock())

    def test_should_map_callables(self):
        assert self.module.routes_binder.calls('connect', '/',
                                                controller=self.controller)

    def test_should_map_methods(self):
        assert self.module.routes_binder.calls('connect', '/foo',
                                                controller=self.controller,
                                                action='bar')
