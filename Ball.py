from PyQt5.QtCore import QPoint
from Central import dV_dx, dV_dy
POINTS_COUNT = 1000

class Ball:

    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.fx = 0;
        self.fy = 0;
        self.m = 1;
        self.points = []
        self.owner = None

    def force(self):
        self.fx = dV_dx(self.x, self.y)
        self.fy = dV_dy(self.x, self.y)

    def move(self):
        ax = self.fx / self.m
        ay = self.fy / self.m
        self.vx += ax
        self.vy += ay
        self.x += self.vx
        self.y += self.vy
        if len(self.points) < POINTS_COUNT:
            self.points.append(QPoint(self.x, self.y));

    def refresh(self, text):
        o = eval('{' + text + '}')
        b = self;
        b.x = o['x']
        b.y = o['y']
        b.vx = o['vx']
        b.vy = o['vy']
        b.points.clear()


