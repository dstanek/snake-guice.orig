from snakeguice.binder import Binder
from snakeguice.errors import BindingError


def describe_a_Binder():

    binder = Binder()
    binder.bind(object, to_instance=object())

    def describe_when_adding_a_duplicate_binding():
        try:
            binder.bind(object, to_instance=object())
            e = None
        except BindingError, e:
            pass

        def then_a_BindingError_is_raised():
            assert isinstance(e, BindingError)
