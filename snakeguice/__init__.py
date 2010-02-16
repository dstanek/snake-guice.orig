"""Main API entry point for snake-guice."""

from snakeguice.injector import Injector
from snakeguice.decorators import inject, annotate, provides
from snakeguice.errors import SnakeGuiceError, BindingError
from snakeguice.interceptors import ParameterInterceptor


# TODO: delete this; i don't really like this anymore; it will die soon
Injected = object() # pylint: disable-msg=C0103
