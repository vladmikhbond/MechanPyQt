import sys
import os.path
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QTimer, QRect, QPoint
from model.Ball import Ball
from model.Central import Central
from ui.mainForm import Ui_MainWindow  # импорт нашего сгенерированного файла
from fieldWidget import FieldWidget
from glWidget import GLWidget


FIELD_SIDE = 700
T_INTERVAL = 20
CELL = 6

SETTINGS = "'kz': 1, 'cell': 6, 'light': 15, 'view': 0"
POTENTIAL = "100 * math.sin(r/ 20)"
CONDITIONS = "'x':100, 'y':0, 'vx':0, 'vy':1"
INI_FILE_PATH = "ini.txt"

class Main(QMainWindow):

    def __init__(self):
        super().__init__()

        # init model
        self.model = Central(FIELD_SIDE, CELL, Ball())

        # init UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.glWidget = GLWidget(self, self.model, SETTINGS)
        self.glWidget.setGeometry(QRect(10, 150, self.model.width, self.model.height))
        self.glWidget.setObjectName("glWidget")

        self.fieldWidget = FieldWidget(self, self.model)
        self.fieldWidget.setGeometry(QRect(10, 150, self.model.width, self.model.height))
        self.fieldWidget.setMouseTracking(True)
        self.fieldWidget.setObjectName("fieldWidget")
        #
        self.loadFromFile()
        self.ui.settings.setPlainText(SETTINGS)
        self.ui.potential.setPlainText(POTENTIAL)
        self.ui.conditions.setPlainText(CONDITIONS)

        self.show()

        # init timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.step)

        # init handlers
        self.setMouseTracking(True)
        self.ui.okButton.clicked.connect(self.okBtnClicked)
        self.ui.okBallButton.clicked.connect(self.okBallBtnClicked)

        # first time drawing
        self.okBtnClicked()
        self.okBallBtnClicked()

    # ========================================== File

    def loadFromFile(self):
        global SETTINGS, POTENTIAL, CONDITIONS
        if os.path.exists(INI_FILE_PATH):
            with open(INI_FILE_PATH, 'r') as f:
                lines = f.readlines()
        if len(lines) >= 3:
            if lines[0]: SETTINGS = lines[0].strip()
            if lines[1]: POTENTIAL = lines[1].strip()
            if lines[2]: CONDITIONS = lines[2].strip()

    def saveToFile(self):
        global SETTINGS, POTENTIAL, CONDITIONS
        with open(INI_FILE_PATH, 'w') as f:
            f.write(SETTINGS + '\n')
            f.write(POTENTIAL + '\n')
            f.write(CONDITIONS + '\n')

    # ========================================== Handlers

    def mousePressEvent(self, event):
        # diagnostic print
        p = self.ScreenToWorld(event.pos())
        v = Central.V(p.x(), p.y())
        n = (v - self.model.Vmin) * self.model.K * self.glWidget.kz
        print(f'x={p.x():4}  y={p.y():4}  v={v:0.4f} z={n:0.4f}')

        # toggle timer
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(T_INTERVAL)

    def ScreenToWorld(self, cur: QPoint):
        x0, y0 = self.model.width / 2, self.model.height / 2
        x = cur.x() - self.fieldWidget.geometry().x()
        y = cur.y() - self.fieldWidget.geometry().y()
        return QPoint(x - x0, y0 - y )

    def okBtnClicked(self):
        global SETTINGS, POTENTIAL
        # renew potential
        POTENTIAL  = self.ui.potential.toPlainText()
        self.model.reset(POTENTIAL )
        self.fieldWidget.createFieldImage()

        # renew settings
        SETTINGS = self.ui.settings.toPlainText()
        self.glWidget.reset(SETTINGS)
        self.glWidget.repaint()

        if self.glWidget.view:
            self.fieldWidget.setVisible(False)
            self.timer.stop()
        else:
            self.fieldWidget.setVisible(True)
            self.timer.start(T_INTERVAL)

        self.saveToFile()

    def okBallBtnClicked(self):
        global CONDITIONS
        # renew a ball
        CONDITIONS = self.ui.conditions.toPlainText()
        self.model.balls[0].reset(CONDITIONS)
        self.fieldWidget.createFieldImage()

        self.timer.start(T_INTERVAL)
        self.saveToFile()

    def step(self):
        # stop timer when a ball is far away
        if self.model.balls[0].r() > self.model.width * 2:
            self.timer.stop()

        # many steps and one painting
        for i in range(10):
            self.model.step()

        self.fieldWidget.repaint()

        # diagnostic: Energy and Lagrangian
        b = self.model.balls[0]
        o = b.lagrangian()
        self.setWindowTitle(f'E = { b.T() + b.V() :12.8f}   L = ({o[0] + o[1]  :12.8f}, {o[2] + o[3]  :12.8f})')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())
