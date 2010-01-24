class Annotation(object):

    def __init__(self, value):
        self._value = value

    def __hash__(self):
        return hash(self.__class__.__name__ + ":" + self._value)

    def __eq__(self, other):
        return (self.__class__ == other.__class__
                and self._value == other._value)

    def __ne__(self, other):
        return not self.__eq__(other)
