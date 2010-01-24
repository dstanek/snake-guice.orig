"""Specification for PrivateModules using the "robot legs" problem."""

from snakeguice import inject, annotate, Injector
from snakeguice.modules import Module, PrivateModule


class IFoot(object): pass
class ILeg(object): pass
class IRobot(object): pass


class LeftFoot(object): pass
class RightFoot(object): pass


class Leg(object):

    @inject(foot=IFoot)
    def __init__(self, foot):
        self.foot = foot


class Robot(object):

    @inject(left_leg=ILeg, right_leg=ILeg)
    @annotate(left_leg="left", right_leg="right")
    def __init__(self, left_leg, right_leg):
        self.left_leg = left_leg
        self.right_leg = right_leg


class LeftModule(PrivateModule):

    def configure(self, binder):
        binder.bind(ILeg, annotated_with="left", to=Leg)
        binder.bind(IFoot, to=LeftFoot)
        self.expose(binder, ILeg, "left")


class RightModule(PrivateModule):

    def configure(self, binder):
        binder.bind(ILeg, annotated_with="right", to=Leg)
        binder.bind(IFoot, to=RightFoot)
        self.expose(binder, ILeg, "right")


class MyModule(Module):

    def configure(self, binder):
        binder.bind(IRobot, to=Robot)
        self.install(binder, LeftModule())
        self.install(binder, RightModule())


def describe_solving_the_robot_legs_problem():

    injector = Injector(MyModule())
    robot = injector.get_instance(IRobot)

    def should_return_an_instance():
        assert isinstance(robot, Robot)

    def should_have_Leg_instances():
        assert isinstance(robot.left_leg, Leg)
        assert isinstance(robot.right_leg, Leg)

    def should_have_the_correct_Feet_instances():
        assert isinstance(robot.left_leg.foot, LeftFoot)
        assert isinstance(robot.right_leg.foot, RightFoot)
