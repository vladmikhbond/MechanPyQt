import os
from model.Settings import Settings

ARCH_FILE = ".arc"

class Arch:
    def __init__(self):
        self.sets = []

    def loadFromFile(self):

        if os.path.exists(ARCH_FILE):
            self.sets = []
            with open(ARCH_FILE, 'r', encoding="utf-8") as f:
                while(1):
                    a = f.readline()
                    if not a:
                        break
                    setting = Settings()
                    setting.reset(a, f.readline(), f.readline())
                    self.sets.append(setting)

    def saveToFile(self):
        with open(ARCH_FILE, 'w', encoding="utf-8") as f:
            for s in self.sets:
                print(s, file=f)


# singleton
archive: Arch = Arch()
archive.loadFromFile()
