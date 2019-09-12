from PyQt5.QtCore import QPoint

POINTS_COUNT = 10008

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

    def step(self):
        ax = self.fx / self.m
        ay = self.fy / self.m
        self.vx += ax
        self.vy += ay
        self.x += self.vx
        self.y += self.vy
        if len(self.points) < POINTS_COUNT:
            self.points.append(QPoint(self.x, self.y));


