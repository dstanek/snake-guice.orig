class Annotation(object):

    def __init__(self, value):
        self._value = value

    def __hash__(self):
        return hash(self.__class__.__name__ + ":" + self._value)

    def __eq__(self, other):
        return self._value == other._value
