import math
import random


class Beam:

    def __init__(self, angle=0, size=1000):
        self.angle = angle
        self.size = size

    def change_angle(self, change):
        self.angle += change


class Ball:
    gravity = 9.7

    def __init__(self, location=0, friction_amount=0.01):
        self.velocity = 0
        self.location = location
        self.friction_amount = friction_amount

    def run_timestep(self, angle):
        # update location
        self.location += self.velocity

        # Calculate new velocity
        angle = math.radians(angle)
        velocity_change = math.sin(angle) * self.gravity

        # Friction
        friction = self.friction_amount * abs(math.cos(angle)) * self.gravity
        if abs(friction) < abs(self.velocity):
            if self.velocity < 0:
                velocity_change += friction
            else:
                velocity_change -= friction
        else:
            self.velocity = 0

        self.velocity = self.velocity + velocity_change


class Model:
    """
    This model encapsulates both the balls and the beam
    """
    def __init__(self, balls=None):
        self.t = 0
        self.beam = Beam()
        self.balls = balls or [Ball(self.beam.size / 2, random.random() / 10) for _ in range(3)]

    def turn_beam_left(self):
        self.beam.change_angle(-2)

    def turn_beam_right(self):
        self.beam.change_angle(2)

    def run_timestep(self):
        for ball in self.balls:
            ball.run_timestep(self.beam.angle)

        self.t += 1
