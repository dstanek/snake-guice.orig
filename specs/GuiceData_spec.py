"""Behavioral tests for the GuiceData implementation."""

from nose.tools import raises

from snakeguice.decorators import GuiceData


def describe_initializing_GuiceData_from_a_class():

    def describe_without_instance_attached():
        class Dummy(object): pass

        data = GuiceData.from_class(Dummy)

        def should_return_a_GuiceData_instance():
            assert isinstance(data, GuiceData)

        def should_save_create_class_attribute():
            assert Dummy.__guice__ is data

    def describe_with_instance_attached():
        existing_data = GuiceData()
        class Dummy(object):
            __guice__ = existing_data

        data = GuiceData.from_class(Dummy)

        def should_return_existing_instance():
            assert existing_data is data

    def describe_when_using_builtin_types():
        data0 = GuiceData.from_class(object)
        data1 = GuiceData.from_class(object)

        def should_return_new_instance_each_time():
            assert data0 is not data1

        def should_not_be_storing_instance():
            assert not hasattr(object, '__guice__')


def test_creating_GuiceData_from_a_class():
    pass


def describe_compositing_GuiceData_instances():

    class GrandDaddy(object): pass
    g_data = GuiceData.from_class(GrandDaddy)
    g_data.init = object()
    g_data.methods = {'g_method': object(),'method': object()}
    
    class Daddy(GrandDaddy): pass
    d_data = GuiceData.from_class(Daddy)
    d_data.init = object()
    d_data.methods = {'d_method': object(),'method': object()}

    class Son(Daddy): pass
    s_data = GuiceData.from_class(Son)
    s_data.init = object()
    s_data.methods = {'s_method': object()}

    data = GuiceData.composite_from_class(Son)

    def should_have_create_a_new_GuiceData_instance():
        assert isinstance(data, GuiceData)
        assert data not in (g_data, d_data, s_data)

    def should_have_all_unique_methods():
        assert data.methods['g_method'] == g_data.methods['g_method']
        assert data.methods['d_method'] == d_data.methods['d_method']
        assert data.methods['s_method'] == s_data.methods['s_method']

    def should_use_the_last_method_defined():
        assert data.methods['method'] == d_data.methods['method']
