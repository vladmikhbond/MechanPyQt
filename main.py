import sys
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
TEST = "100 *  math.sin(r/ 20)"
#TEST = "0.00005 * r**2"

class Main(QMainWindow):

    def __init__(self):
        super().__init__()

        # init model
        self.model = Central(FIELD_SIDE, FIELD_SIDE, CELL, Ball())

        # init UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.glWidget = GLWidget(self, self.model)
        self.glWidget.setGeometry(QRect(10, 150, self.model.width, self.model.height))
        self.glWidget.setObjectName("glWidget")

        self.fieldWidget = FieldWidget(self, self.model)
        self.fieldWidget.setGeometry(QRect(10, 150, self.model.width, self.model.height))
        self.fieldWidget.setMouseTracking(True)
        self.fieldWidget.setObjectName("fieldWidget")
        #
        self.ui.potential.setPlainText(TEST)
        self.ui.settings.setPlainText("'kz': 1, 'phi': 0")

        self.show()

        # init timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.step)

        # init handlers
        self.setMouseTracking(True)
        self.ui.okButton.clicked.connect(self.okBtnClicked)

        # first time drawing
        self.okBtnClicked()

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
        # renew potential
        text = self.ui.potential.toPlainText()
        self.model.reset(text)   #todo: danger - div by zero
        self.fieldWidget.createFieldImage()
        self.glWidget.repaint()
        # renew a ball
        text = self.ui.conditions.toPlainText()
        self.model.balls[0].reset(text)
        # renew settings
        text = self.ui.settings.toPlainText()
        self.glWidget.reset(text)
        self.glWidget.repaint()

        self.timer.start(T_INTERVAL)

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
