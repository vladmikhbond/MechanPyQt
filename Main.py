import sys, math
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QPixmap
from PyQt5.QtCore import QTimer, QPoint
from model.Ball import Ball
from model.Central import Central
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

        # init handlers
        self.setMouseTracking(True)
        self.ui.okButton.clicked.connect(self.okBtnClicked)

        # init model
        self.width()
        self.central = Central(self.width(), self.height(), Ball())
        self.okBtnClicked()

    # ========================================== Handlers

    def mousePressEvent(self, event):
        p = self.central.ScreenToWorld(event.pos())
        v = Central.V(p.x(), p.y())
        print(p.x(), p.y(), v)

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
        self.backImage = self.createFieldImage()

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
        self.drawField()
        self.drawBalls()

    def drawField(self):
        if self.backImage:
            qp = QPainter()
            qp.begin(self)
            qp.drawPixmap(0, 0, self.backImage)
            qp.end()

    def createFieldImage111(self):
        pix = QPixmap(self.central.width, self.central.height)
        qp = QPainter()
        qp.begin(pix)
        qp.translate(self.central.width / 2, self.central.height / 2)
        qp.scale(1, -1)

        dx = 4
        xLimit = round(self.central.width / 1.00)
        xs = [x for x in range(1, xLimit, dx)]
        vs = [math.log(abs(Central.V(x + dx/2, 0))) for x in range(0, xLimit, dx)]
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
        # qp.drawEllipse(QPoint(0, 0), 5, 5)
        qp.end()

        return pix

    def createFieldImage(self):
        pix = QPixmap(self.central.width, self.central.height)
        qp = QPainter()
        qp.begin(pix)
        qp.translate(self.central.width / 2, self.central.height / 2)
        qp.scale(1, -1)

        X = self.central.width // 2 - 1
        Y = self.central.height // 2 - 1
        D = 6
        vmin = vmax = abs(Central.V(-X, -Y))
        for x in range(-X, X, D):
            for y in range(-Y, Y, D):
                v = abs(Central.V(x, y))
                if vmin > v: vmin = v
                if vmax < v: vmax = v
        k = 255 / (vmax - vmin)

        for x in range(-X, X, D):
            for y in range(-Y, Y, D):
                v = Central.V(x, y)
                color = 255 - k * (abs(v) - vmin)
                qcolor = QColor(color, color, 255)
                qp.setPen(qcolor)
                qp.setBrush(qcolor)
                qp.drawRect(x - D/2, y - D/2, D, D)

        # draw Center
        qp.setPen(QPen(QBrush(BALL_COLOR), 1))
        qp.setBrush(SUN_COLOR)
        qp.drawEllipse(QPoint(0, 0), 5, 5)
        qp.end()

        return pix



    def drawBalls(self):
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
