#!python

from dingus import Dingus, DingusTestCase

from snakeguice import config


class __TestConfig(DingusTestCase(config.Config)):

    def setup(self):
        super(TestConfig, self).setup()

        self.s = 'some string value'
        self.c = config.Config(self.s)

    def test(self):
        assert self.c.entry == self.s
