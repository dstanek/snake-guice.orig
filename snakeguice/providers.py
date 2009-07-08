"""Providers used in the binding process."""
# pylint: disable-msg=C0111
#         providers are so small that we can safely omit doc comments


class SimpleProvider(object):

    def __init__(self, injector, cls):
        self._injector = injector
        self._class = cls

    def get(self):
        return self._injector.create_object(self._class)


class InstanceProvider(object):

    def __init__(self, obj):
        self._obj = obj

    def get(self):
        return self._obj


class ProviderProvider(object):

    def __init__(self, injector, provider):
        self._injector = injector
        self._provider = provider

    def get(self):
        return self._injector.get_instance(self._provider).get()
