from snakeguice import create_injector, inject
from snakeguice.interfaces import Injector
from snakeguice.multibinder import ListBinder, List, DictBinder, Dict
from snakeguice import providers


class ISnack(object):
    """A snack interface."""


class Twix(object):
    """A concrete snack implementation."""


class Snickers(object):
    """A concrete snack implementation."""


class Skittles(object):
    """A concrete snack implementation."""


class Lays(object):
    """A concrete snack implementation."""


class Tostitos(object):
    """A concrete snack implementation."""


class Ruffles(object):
    """A concrete snack implementation."""


class ListCandyModule(object):
    """One to two modules adding to the multibinder."""

    def configure(self, binder):
        listbinder = ListBinder(binder, ISnack)
        listbinder.add_binding(to=Twix)
        provider = providers.create_simple_provider(Snickers)
        listbinder.add_binding(to_provider=provider)
        listbinder.add_binding(to_instance=Skittles())


class ListChipsModule(object):
    """One to two modules adding to the multibinder."""

    def configure(self, binder):
        listbinder = ListBinder(binder, ISnack)
        listbinder.add_binding(to=Lays)
        provider = providers.create_simple_provider(Tostitos)
        listbinder.add_binding(to_provider=provider)
        listbinder.add_binding(to_instance=Ruffles())


class ListSnackMachine(object):

    @inject(snacks=List(ISnack))
    def __init__(self, snacks):
        self.snacks = snacks


class DictCandyModule(object):
    """One to two modules adding to the multibinder."""

    def configure(self, binder):
        dictbinder = DictBinder(binder, ISnack)
        dictbinder.add_binding('twix', to=Twix)
        provider = providers.create_simple_provider(Snickers)
        dictbinder.add_binding('snickers', to_provider=provider)
        dictbinder.add_binding('skittles', to_instance=Skittles())


class DictChipsModule(object):
    """One to two modules adding to the multibinder."""

    def configure(self, binder):
        dictbinder = DictBinder(binder, ISnack)
        dictbinder.add_binding('lays', to=Lays)
        provider = providers.create_simple_provider(Tostitos)
        dictbinder.add_binding('tostitos', to_provider=provider)
        dictbinder.add_binding('ruffles', to_instance=Ruffles())


class DictSnackMachine(object):

    @inject(snacks=Dict(ISnack))
    def __init__(self, snacks):
        self.snacks = snacks


SNACK_CLASSES = (Twix, Snickers, Skittles, Lays, Tostitos, Ruffles)


class base_multibinder(object):

    def test_that_the_injected_value_has_the_correct_number_of_elements(self):
        assert len(self.snack_machine.snacks) == len(SNACK_CLASSES)


class test_using_ListBinder(base_multibinder):

    def setup(self):
        injector = create_injector([ListCandyModule(), ListChipsModule()])
        self.snack_machine = injector.get_instance(ListSnackMachine)

    def test_that_the_elements_have_the_correct_type(self):
        for n, snack in enumerate(self.snack_machine.snacks):
            assert isinstance(snack, SNACK_CLASSES[n])


class test_using_DictBinder(base_multibinder):

    def setup(self):
        injector = create_injector([DictCandyModule(), DictChipsModule()])
        self.snack_machine = injector.get_instance(DictSnackMachine)

    def test_that_the_elements_have_the_correct_type(self):
        for k, v in self.snack_machine.snacks.items():
            assert k == v.__class__.__name__.lower()
            assert v.__class__ in SNACK_CLASSES
