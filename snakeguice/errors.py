#!/usr/bin/env python

"""errors used by snake-guice"""


class SnakeGuiceError(Exception):
    """Base for all of our errors."""


class BindingError(SnakeGuiceError):
    """Raised when an issue in the binding rules is found."""
