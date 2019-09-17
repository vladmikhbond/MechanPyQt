from PyQt5.QtCore import QPoint
from model.Central import dV_dx, dV_dy, Central


POINTS_COUNT = 10000

class Ball:

    def __init__(self, x=0, y=0, vx=0, vy=0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.fx = 0
        self.fy = 0
        self.m = 1

        self.shadowX = None
        self.shadowY = None
        self.owner = None

    def force(self):
        self.fx = - dV_dx(self.x, self.y)
        self.fy = - dV_dy(self.x, self.y)

    def move(self):
        ax = self.fx / self.m
        ay = self.fy / self.m
        self.vx += ax
        self.vy += ay
        self.x += self.vx
        self.y += self.vy

    def refresh(self, text):
        o = eval('{' + text + '}')
        b = self;
        b.x = o['x']
        b.y = o['y']
        b.vx = o['vx']
        b.vy = o['vy']
        b.shadowX = None
        b.shadowY = None

    def r(self):
        return (self.x * self.x + self.y * self.y) ** 0.5

    def T(self):
        return (self.vx * self.vx + self.vy * self.vy) * self.m / 2

    def V(self):
        return Central.V(self.x, self.y)
