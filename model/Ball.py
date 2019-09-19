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

        self._x = None
        self._y = None
        self._vx = None
        self._vy = None
        self.owner = None

    def force(self):
        self.fx = - dV_dx(self.x, self.y)
        self.fy = - dV_dy(self.x, self.y)

    def move(self):
        self._x = self.x
        self._y = self.y
        self._vx = self.vx
        self._vy = self.vy

        ax = self.fx / self.m
        ay = self.fy / self.m
        self.vx += ax
        self.vy += ay
        self.x += self.vx
        self.y += self.vy

    def refresh(self, text):
        o = eval('{' + text + '}')
        self.x = o['x']
        self.y = o['y']
        self.vx = o['vx']
        self.vy = o['vy']
        self._x = None


    def r(self):
        return (self.x * self.x + self.y * self.y) ** 0.5

    def T(self):
        return (self.vx * self.vx + self.vy * self.vy) * self.m / 2

    def V(self):
        return Central.V(self.x, self.y)


    def lagrangian(self):
        px, py = self.m * self.vx, self.m * self.vy
        p_x, p_y = self.m * self._vx, self.m * self._vy
        dpx_dt, dpy_dt = (px - p_x) / 1, (py - p_y) / 1

        dV_dx = (Central.V(self.x, self.y) - Central.V(self._x, self.y)) / (self.x - self._x)
        dV_dy = (Central.V(self.x, self.y) - Central.V(self.x, self._y)) / (self.y - self._y)
        return [
            dpx_dt, dV_dx,
            dpy_dt, dV_dy ]

