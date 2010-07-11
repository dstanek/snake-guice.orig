"""Scopes that can be used in the binding process."""

# pylint: disable-msg=C0111

from snakeguice import providers


class _NoScope(object):
    """A default scrope returns the same provider that gets passed in.
    
    This is internally used and will probably never be directly used in 
    a module.
    """

    def scope(self, key, unscoped_provider): # pylint: disable-msg=R0201,W0613
        return unscoped_provider


class _Singleton(object):
    """A singleton scope only allows a single instance to be created for a
    given key.
    """

    def __init__(self):
        self._cached_provider_map = {}

    def scope(self, key, provider):
        cached_provider = self._cached_provider_map.get(key)
        if not cached_provider:
            instance = provider.get()
            cached_provider = self._cached_provider_map[key] = \
                    providers.create_instance_provider(instance)
        return cached_provider


NO_SCOPE = _NoScope()
SINGLETON = _Singleton()
