DELTA = 0.01

def dV_dx(x, y):
    return (Central.V(x + DELTA, y) - Central.V(x - DELTA, y)) / (2 * DELTA)


def dV_dy(x, y):
    return (Central.V(x, y + DELTA) - Central.V(x, y - DELTA)) / (2 * DELTA)


class Central:

    V = None

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
        Central.V = eval("lambda x, y: " + text)

