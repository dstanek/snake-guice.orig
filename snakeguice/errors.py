"""Errors used by snake-guice"""


class SnakeGuiceError(Exception):
    """Base for all of our errors."""


class BindingError(SnakeGuiceError):
    """Raised when an issue in the binding rules is found."""


class AssistError(SnakeGuiceError):
    """Raised when an issue with assisted injection is found."""


class MultiBindingError(SnakeGuiceError):
    """Raised when a issue with multi-binding is found."""
