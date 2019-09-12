class Ball:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.fx = 0;
        self.fy = 0;
        self.m = 1;

    def step(self):
        ax = self.fx / self.m
        ay = self.fy / self.m
        self.vx += ax
        self.vy += ay
        self.x += self.vx
        self.y += self.vy



