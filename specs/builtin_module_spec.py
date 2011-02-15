from snakeguice import create_injector, inject
from snakeguice.interfaces import Injector


def given_an_empty_injector():

    inj = create_injector([])

    def when_requesting_an_Injector_instance():

        class Awesome(object):
            @inject(injector=Injector)
            def __init__(self, injector):
                self.injector = injector

        awesome = inj.get_instance(Awesome)

        def then_the_injector_itself_is_used():
            print awesome.injector
            assert awesome.injector is inj
