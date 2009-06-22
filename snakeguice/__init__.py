#!/usr/bin/env python

from snakeguice.injector import Injector
from snakeguice.decorators import inject
from snakeguice.errors import SnakeGuiceError, BindingError
from snakeguice.interceptors import ParameterInterceptor


Injected = object()
