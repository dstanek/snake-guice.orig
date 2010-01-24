from snakeguice.annotation import Annotation


class test_Annotations_with_equal_values(object):

    @classmethod
    def setup_class(cls):
        cls.annotation0 = Annotation('value here')
        cls.annotation1 = Annotation('value here')

    def test_hash_the_same(self):
        assert hash(self.annotation0) == hash(self.annotation1)

    def test_should_be_equal(self):
        assert self.annotation0 == self.annotation1


class test_Annotations_without_equal_values(object):

    @classmethod
    def setup_class(cls):
        cls.annotation0 = Annotation('value here0')
        cls.annotation1 = Annotation('value here1')

    def test_should_hash_differently(self):
        assert hash(self.annotation0) != hash(self.annotation1)

    def test_should_not_be_equal(self):
        assert self.annotation0 != self.annotation1


class test_comparing_different_Annotation_subclasses(
        test_Annotations_without_equal_values):

    @classmethod
    def setup_class(cls):
        class Annotation0(Annotation): pass
        class Annotation1(Annotation): pass

        cls.annotation0 = Annotation0('value here')
        cls.annotation1 = Annotation1('value here')
