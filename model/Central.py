# import math is needed for V evaluation
import math
from model.Settings import settings as ss


_delta = 0.001

def dV_dx(x, y):
    return (Central.V(x + _delta, y) - Central.V(x - _delta, y)) / (2 * _delta)


def dV_dy(x, y):
    return (Central.V(x, y + _delta) - Central.V(x, y - _delta)) / (2 * _delta)


class Central:

    V = lambda x, y: None

    def __init__(self, side, cell, *balls):
        self.width = side
        self.height = side
        self.balls = []
        self.cell = cell
        for b in balls:
            self.addBall(b)

    def step(self):
        for b in self.balls:
            b.force()
        for b in self.balls:
            b.move()

    def addBall(self, ball):
        ball.owner = self
        self.balls.append(ball)

    def reset(self, ss):
        text = ss.V.replace("r", "((x*x + y*y)**0.5)")
        Central.V = eval("lambda x, y: " + text)
        self.balls[0].reset(ss)
