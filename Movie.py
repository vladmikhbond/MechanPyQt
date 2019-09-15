import sys, math
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QPixmap
from PyQt5.QtCore import QTimer, QPoint, QRectF
from Ball import Ball
from Central import Central
from ui.mainForm import Ui_MainWindow  # импорт нашего сгенерированного файла

T_INTERVAL = 20
TRACK_COLOR = QColor('black')
BALL_COLOR = QColor('red')
SUN_COLOR = QColor('yellow')


class Movie(QMainWindow):

    def __init__(self):
        super().__init__()
        self.backImage = None

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()

        # init timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.step)

        # init model
        self.width()
        self.central = Central(self.width(), self.height(), Ball(x=0, y=0, vx=0, vy=0))

        # init handlers
        self.setMouseTracking(True)
        self.ui.okButton.clicked.connect(self.okBtnClicked)
        self.okBtnClicked()



    # ========================================== Handlers

    def mousePressEvent(self, event):
        # p = self.central.ScreenToWorld(event.pos())
        # v = Central.V(p.x(), p.y())
        # print(p.x(), p.y(), v)

        # toggle timer
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(T_INTERVAL)

    def okBtnClicked(self):
        # renew potential
        text = self.ui.potential.toPlainText()
        text = text.replace("r", "((x*x + y*y)**0.5)")
        self.central.refresh(text)
        self.backImage = self.createBackImage()

        # renew a ball
        text = self.ui.conditions.toPlainText()
        self.central.balls[0].refresh(text)
        self.timer.start(T_INTERVAL)

    def step(self):
        # stop timer when a ball is far away
        if self.central.balls[0].r() > self.central.width:
            self.timer.stop()

        # many steps and one painting
        for i in range(10):
            self.central.step()
        self.repaint()

        # energy diagnostic

        e = self.central.T() - self.central.v()
        self.setWindowTitle(f'E = {e:12.8f}')

    # ========================================== Painting

    def paintEvent(self, event):
        self.drawBack()
        self.drawFront()

    def drawBack(self):
        if self.backImage:
            qp = QPainter()
            qp.begin(self)
            qp.drawPixmap(0, 0, self.backImage)
            qp.end()

    def createBackImage(self):
        pix = QPixmap(self.central.width, self.central.height)
        qp = QPainter()
        qp.begin(pix)
        qp.translate(self.central.width / 2, self.central.height / 2)
        qp.scale(1, -1)

        # qp.setPen(QColor(0xCC, 0xCC, 0xCC))
        dx = 10
        xLimit = round(self.central.width / 1.00)
        xs = [x for x in range(1, xLimit, dx)]
        vs = [math.log(abs(Central.V(x, 0))) for x in range(1, xLimit, dx)]
        vmax, vmin = max(*vs), min(*vs)
        k = 256 / (vmax - vmin)

        for x, v in zip(xs, vs):
            color = 256 - k * (v - vmin)
            pen = QPen(QBrush(QColor(color, color, 255)), dx + 1)
            qp.setPen(pen)
            qp.drawEllipse(QPoint(0, 0), x, x)

        # draw Center
        qp.setPen(QPen(QBrush(BALL_COLOR), 1))
        qp.setBrush(SUN_COLOR)
        qp.drawEllipse(QPoint(0, 0), 5, 5)
        qp.end()

        return pix

    def drawFront(self):
        qp = QPainter()
        qp.begin(self)
        qp.translate(self.central.width / 2, self.central.height / 2)
        qp.scale(1, -1)

        qp.setPen(TRACK_COLOR)
        for b in self.central.balls:
            for p in b.points:
                qp.drawPoint(p)

        qp.setPen(BALL_COLOR)
        qp.setBrush(BALL_COLOR)
        r = 10
        for b in self.central.balls:
            qp.drawEllipse(QPoint(b.x, b.y), r, r)

        qp.end()

# ========================================== Main

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Movie()
    sys.exit(app.exec_())
