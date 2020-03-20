import math
import random

from social_choice_functions import Plurality


class Beam:

    def __init__(self, angle=0, size=1000):
        self.angle = angle
        self.size = size

    def change_angle(self, change):
        self.angle += change


class Ball:
    gravity = 4.85  # 9.7
    LEFT_BALLOT = ['left', 'right']
    RIGHT_BALLOT = ['right', 'left']

    def __init__(self, name, location=0, friction_amount=0.01):
        self.velocity = 0
        self.location = location
        self.friction_amount = friction_amount
        self.name = name
        self.active = True

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
    
    def get_ballot(self, model):
        if model.beam.angle > 0:
            if self.location > (1 - model.beam.angle / 10) * model.beam.size:
                return self.LEFT_BALLOT
        elif model.beam.angle < 0:
            if self.location < (abs(model.beam.angle) / 10) * model.beam.size:
                return self.RIGHT_BALLOT

        balls_left = sum(1 for b in model.balls if b.location < self.location)
        balls_right = sum(1 for b in model.balls if b.location > self.location)

        if balls_left > balls_right:
            return self.LEFT_BALLOT
        elif balls_right > balls_left:
            return self.RIGHT_BALLOT
        else:
            return self.LEFT_BALLOT if random.random() < .5 else self.RIGHT_BALLOT

    def inactivate(self):
        self.active = False


class Model:
    """
    This model encapsulates both the balls and the beam
    """
    def __init__(self, balls=None, social_choice_function=Plurality, verbose=True, vote_interval=20):
        self.vote_interval = vote_interval
        self.verbose = verbose
        self.social_choice_function = social_choice_function(verbose)
        self.t = 0
        self.beam = Beam()
        ball_pos_min, ball_pos_max = self.beam.size * 0.25, self.beam.size * 0.75
        self.balls = balls or [
            Ball(
                name=i,
                location=random.randint(ball_pos_min, ball_pos_max),  # self.beam.size // 2,
                friction_amount=random.random() / 10
            ) for i in range(10)
        ]

    @property
    def active_balls(self):
        return [b for b in self.balls if b.active]

    def turn_beam_left(self):
        self.beam.change_angle(-1)

    def turn_beam_right(self):
        self.beam.change_angle(1)

    def run_timestep(self):
        for ball in self.active_balls:
            if ball.location < 0 or ball.location > self.beam.size:
                ball.inactivate()

        for ball in self.active_balls:
            ball.run_timestep(self.beam.angle)

        if self.t % self.vote_interval == 0:
            current_profile = self.create_profile(self.active_balls)
            self.move_beam_by_social_choice(current_profile)

        self.t += 1

    def create_profile(self, agents):
        return [agent.get_ballot(self) for agent in agents]

    def move_beam_by_social_choice(self, profile):
        social_choice = self.social_choice_function(profile)
        if social_choice == 'left':
            self.turn_beam_left()
        elif social_choice == 'right':
            self.turn_beam_right()
        else:
            raise RuntimeError('Social choice was not left nor right')
