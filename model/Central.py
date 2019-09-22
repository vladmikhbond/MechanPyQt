import math
DELTA = 0.001
from PyQt5.QtCore import QPoint

def dV_dx(x, y):
    return (Central.V(x + DELTA, y) - Central.V(x - DELTA, y)) / (2 * DELTA)


def dV_dy(x, y):
    return (Central.V(x, y + DELTA) - Central.V(x, y - DELTA)) / (2 * DELTA)


class Central:

    V = lambda x, y: 0


    # def ScreenToWorld(self, p: QPoint):
    #     x0, y0 = self.width / 2, self.height / 2
    #     return QPoint(p.x() - x0, y0 - p.y() )

    def __init__(self, width, height, cell, *balls):
        self.width = width
        self.height = height
        self.balls = []
        self.cell = cell
        for b in balls:
            self.addBall(b)
        self.K = 0

    def step(self):
        for b in self.balls:
            b.force()
        for b in self.balls:
            b.move()

    def addBall(self, ball):
        ball.owner = self
        self.balls.append(ball)

    def reset(self, text):
        text = text.replace("r", "((x*x + y*y)**0.5)")
        Central.V = eval("lambda x, y: " + text)
        self.K = self._calcK();

    def _calcK(self):
        w = self.width // 2
        h = self.height // 2
        d = self.cell

        v_min = v_max = Central.V(-w, -h)
        for x in range(-w, w, d):
            for y in range(-h, h, d):
                v = Central.V(x, y)
                if v_min > v:
                    v_min = v
                if v_max < v:
                    v_max = v
        if v_max == v_min:
            return 0
        return 100 / (v_max - v_min)