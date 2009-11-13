from snakeguice.scopes import _NoScope, _Singleton


class FakeProvider(object):

    def get(self):
        return object()


class test_the_NoScope_scope(object):

    def setup(self):
        self.provider = FakeProvider()
        self.scope = _NoScope()

    def test_that_the_provider_is_passed_through(self):
        assert self.scope.scope('key', self.provider) is self.provider


class test_the_Singleton_scope(object):

    def setup(self):
        self.key = 'key'
        self.provider = FakeProvider()
        self.scope = _Singleton()
        self.scope.scope(self.key,self.provider)

    def test_using_the_same_key_results_in_getting_a_cached_provider(self):
        instance_provider_0 = self.scope.scope(self.key, self.provider)
        instance_provider_1 = self.scope.scope(self.key, self.provider)
        assert instance_provider_0 ==instance_provider_1
