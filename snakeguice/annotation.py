class Annotation(object):
    """Base class for all annotations."""

    def __init__(self, value):
        self._value = str(value)

    def __hash__(self):
        return hash(self.__class__.__name__ + ":" + self._value)

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __ne__(self, other):
        return not self == other
