from nose.tools import raises
from dingus import Dingus, DingusTestCase

from snakeguice.extras import snakeweb


class TestRoutesModuleSetup(DingusTestCase(snakeweb.RoutesModule)):

    def setup(self):
        super(TestRoutesModuleSetup, self).setup()

        class MyRoutesModule(snakeweb.RoutesModule):
            configure_mapper = Dingus()

        self.binder = Dingus()
        self.module = MyRoutesModule()
        self.module.configure(binder=self.binder)

    def test_configure_mapper_is_called_with_a_mapper(self):
        assert self.module.configure_mapper.calls('()',
                snakeweb.RoutesBinder.return_value)

    def test_real_routes_mapper_was_created(self):
        assert snakeweb.routes.Mapper.calls()


class TestRoutesModuleIsAbstract(DingusTestCase(snakeweb.RoutesModule)):

    def setup(self):
        super(TestRoutesModuleIsAbstract, self).setup()
        self.module = snakeweb.RoutesModule()

    @raises(NotImplementedError)
    def test_configure_mapper_is_not_implemented(self):
        self.module.configure(Dingus())


class BaseTestRoutesBinder(DingusTestCase(snakeweb.RoutesBinder)):

    def setup(self):
        super(BaseTestRoutesBinder, self).setup()
        self.routes_mapper = Dingus()
        self.annotation = Dingus()
        self.binder = snakeweb.RoutesBinder(self.routes_mapper, self.annotation)


class TestRoutesBinderConnectWithInvalidControllers(BaseTestRoutesBinder):

    @raises(TypeError)
    def test_an_exception_is_raised_is_no_controller_is_specified(self):
        self.binder.connect('/post/3/view')

    @raises(TypeError)
    def test_an_exception_is_raised_when_a_non_type_controller_is_passed_in(self):
        self.binder.connect('/post/3/view', controller=object())


class TestWhenCallingRoutesBinder(BaseTestRoutesBinder):

    def setup(self):
        super(TestWhenCallingRoutesBinder, self).setup()
        self.controller = object
        self.args = (Dingus(), Dingus())
        self.kwargs = dict(a=Dingus(), controller=object)
        self.binder.connect(*self.args, **self.kwargs)

        self.key = unicode(str(self.controller))
        self.kwargs['controller'] = self.key

    def test_pass_through_to_real_mapper(self):
        assert self.routes_mapper.calls('connect', *self.args, **self.kwargs)

    def test_controller_should_be_added_to_the_map(self):
        assert self.binder.controller_map == {self.key: self.controller}
