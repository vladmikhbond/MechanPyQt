import os

INI_FILE = ".ini"

class Settings:
    def __init__(self):
        # default settings
        self.kz = 1
        self.cell = 6
        self.light = 0
        self.view = 0
        self.V = "100 *  math.sin(r/ 20)"

    def loadFromFile(self):
        if os.path.exists(INI_FILE):
            with open(INI_FILE, 'r') as f:
                self.kz = float(f.readline())
                self.cell = int(f.readline())
                self.light = int(f.readline())
                self.view = int(f.readline())
                self.V = f.readline()

    def saveToFile(self):
        with open(INI_FILE, 'w') as f:
            print(self.kz, file=f)
            print(self.cell, file=f)
            print(self.light, file=f)
            print(self.view, file=f)
            print(self.V, file=f)

    #  "kz=1.1, cell=7, light=10, view=10"
    def paramsToStr(self):
        return f"kz={self.kz}, cell={self.cell}, light={self.light}, view={self.view}"

    def strToParams(self, s):
        eqs = [x.split('=') for x in s.split(',')]
        for k, v in eqs:
            v = float(v.strip()) if "kz" in k else int(v.strip())
            setattr(self, k.strip(), v)
        pass





settings = Settings()
settings.strToParams("kz=1.1, cell=6, light=0, view=0")
