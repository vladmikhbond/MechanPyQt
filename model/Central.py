DELTA = 0.001
from PyQt5.QtCore import QTimer, QPoint, Qt

def dV_dx(x, y):
    return (Central.V(x + DELTA, y) - Central.V(x - DELTA, y)) / (2 * DELTA)


def dV_dy(x, y):
    return (Central.V(x, y + DELTA) - Central.V(x, y - DELTA)) / (2 * DELTA)


class Central:

    V = lambda x, y: 0


    def ScreenToWorld(self, p: QPoint):
        x0, y0 = self.width / 2, self.height / 2
        return QPoint(p.x() - x0, y0 - p.y() )

    def __init__(self, width, height, *balls):
        self.width = width
        self.height = height
        self.balls = []
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

    def refresh(self, text):
        text = text.replace("r", "((x*x + y*y)**0.5)")
        f = eval("lambda x, y: " + text)

        if self.isValid(f):
            Central.V = f
            return True
        return False


    def isValid(self, f):
        X = self.width // 2 - 1
        Y = self.height // 2 - 1
        D = 6
        try:
            for x in range(-X, X, D):
                for y in range(-Y, Y, D):
                    f(x, y)
        except:
            return False
        else:
            return True





    def T(self):
        return sum(b.T() for b in self.balls)

    def v(self):
        return sum(b.V() for b in self.balls)
