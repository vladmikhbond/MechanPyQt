import os
from model.Setting import Setting

ARCH_FILE = ".arc"


class Archive(list):

    def loadFromFile(self):
        if os.path.exists(ARCH_FILE):
            self.clear()
            with open(ARCH_FILE, 'r', encoding="utf-8") as f:
                line = f.readline()
                while line:
                    setting = Setting()
                    setting.reset(line, f.readline(), f.readline())
                    self.append(setting)
                    line = f.readline()

    def saveToFile(self):
        with open(ARCH_FILE, 'w', encoding="utf-8") as f:
            for s in self:
                print(s, file=f)


# singleton
archive: Archive = Archive()
archive.loadFromFile()
