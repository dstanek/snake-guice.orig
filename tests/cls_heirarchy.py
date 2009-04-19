#!/usr/bin/env python

"""
Sample class heirarchy used in the unit tests
"""


class Person(object): pass
class GoodPerson(Person): pass
class EvilPerson(Person): pass

class Place(object): pass
class Beach(Place): pass
class Glacier(Place): pass

class Logger(object): pass
class ConcreteLogger(Logger): pass
