import os

INI_FILE = ".ini"

class Setting:
    def __init__(self):
        # default values
        self.kz = 1
        self.cell = 6
        self.light = 0
        self.view = 0
        #
        self.V = "100 *  math.sin(r/ 20)"
        #
        self.ball_x = 100
        self.ball_y = 0
        self.ball_vx = 0
        self.ball_vy = 1

    # def getComment(self):
    #     i = self.V.rindex("#")
    #     if i != -1:
    #         return self.V[i::]
    #     return ""

    def loadFromFile(self):
        if os.path.exists(INI_FILE):
            with open(INI_FILE, 'r', encoding="utf-8") as f:
                self.kz = float(f.readline())
                self.cell = int(f.readline())
                self.light = int(f.readline())
                self.view = int(f.readline())
                self.V = f.readline()
                self.ball_x = float(f.readline())
                self.ball_y = float(f.readline())
                self.ball_vx = float(f.readline())
                self.ball_vy = float(f.readline())

    def saveToFile(self):
        with open(INI_FILE, 'w', encoding="utf-8") as f:
            print(self.kz, file=f)
            print(self.cell, file=f)
            print(self.light, file=f)
            print(self.view, file=f)
            print(self.V, file=f)
            print(self.ball_x, file=f)
            print(self.ball_y, file=f)
            print(self.ball_vx, file=f)
            print(self.ball_vy, file=f)


    def paramsToStr(self):
        #  "kz=1.1, cell=7, light=10, view=10"
        return f"kz={self.kz}, cell={self.cell}, light={self.light}, view={self.view}"

    def ballToStr(self):
        return f"x={self.ball_x}, y={self.ball_y}, vx={self.ball_vx}, vy={self.ball_vy}"


    def __str__(self):
        return self.paramsToStr() + "\n" + self.V + "\n" + self.ballToStr()

    def reset(self, paramStr, potentStr, ballStr):
        eqs = [x.split('=') for x in paramStr.split(',')]
        for k, v in eqs:
            v = float(v.strip()) if "kz" in k else int(v.strip())
            setattr(self, k.strip(), v)

        self.V = potentStr.strip()

        eqs = [x.split('=') for x in ballStr.split(',')]
        for k, v in eqs:
            setattr(self, "ball_" + k.strip(), float(v.strip()))

        self.saveToFile()

# singleton
setting = Setting()
setting.loadFromFile()
