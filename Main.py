import sys
import math
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QPixmap
from PyQt5.QtCore import QTimer, QPoint
from model.Ball import Ball
from model.Central import Central
from ui.mainForm import Ui_MainWindow  # импорт нашего сгенерированного файла

T_INTERVAL = 20
TRACK_COLOR = QColor('red')
BALL_COLOR = QColor('red')
SUN_COLOR = QColor('yellow')


class Movie(QMainWindow):

    def __init__(self):
        super().__init__()
        self.fieldImage = None

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
        print(f'x={p.x():4}  y={p.y():4}  v={v:0.4f}')

        # toggle timer
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(T_INTERVAL)

    def okBtnClicked(self):
        # renew potential
        text = self.ui.potential.toPlainText()
        if self.central.refresh(text):
            self.createFieldImage()
        else:
            print("ERROR")

        # renew a ball
        text = self.ui.conditions.toPlainText()
        self.central.balls[0].refresh(text)
        self.timer.start(T_INTERVAL)

    def step(self):
        # stop timer when a ball is far away
        if self.central.balls[0].r() > self.central.width * 2:
            self.timer.stop()

        # many steps and one painting
        for i in range(10):
            self.central.step()
        self.repaint()

        # energy diagnostic
        e = self.central.T() + self.central.v()
        self.setWindowTitle(f'E = {e:12.8f}')

    # ========================================== Drawing

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        if self.fieldImage:
            qp.drawPixmap(0, 0, self.fieldImage)

        # balls
        qp.translate(self.central.width / 2, self.central.height / 2)
        qp.scale(1, -1)
        qp.setPen(BALL_COLOR)
        qp.setBrush(BALL_COLOR)
        r = 10
        for b in self.central.balls:
            qp.drawEllipse(QPoint(b.x, b.y), r, r)
        qp.end()

        # tracks to image
        qpi = QPainter()
        qpi.begin(self.fieldImage)
        qpi.translate(self.central.width / 2, self.central.height / 2)
        qpi.scale(1, -1)
        qpi.setPen(TRACK_COLOR)
        for b in self.central.balls:
            if b.prevX:
                qpi.drawLine(b.x, b.y, b.prevX, b.prevY)
            b.prevX = b.x
            b.prevY = b.y

        qpi.end()

    def createFieldImage(self):
        self.fieldImage = QPixmap(self.central.width, self.central.height)
        qp = QPainter()
        qp.begin(self.fieldImage)
        qp.translate(self.central.width / 2, self.central.height / 2)
        qp.scale(1, -1)

        w = self.central.width // 2 - 1
        h = self.central.height // 2 - 1
        d = 6
        v_min = v_max = Central.V(-w, -h)
        for x in range(-w, w, d):
            for y in range(-h, h, d):
                v = Central.V(x, y)
                if v_min > v:
                    v_min = v
                if v_max < v:
                    v_max = v
        if v_max == v_min:
            return

        for x in range(-w, w, d):
            for y in range(-h, h, d):
                v = Central.V(x, y)
                color = 255 - 255 * (v - v_min) / (v_max - v_min)
                q_color = QColor(color, color,  255)

                qp.setPen(q_color)
                qp.setBrush(q_color)
                qp.drawRect(x - d/2, y - d/2, d, d)

        # draw Center
        qp.setPen(QPen(QBrush(BALL_COLOR), 1))
        qp.setBrush(SUN_COLOR)
        qp.drawEllipse(QPoint(0, 0), 5, 5)

        # draw V-profile
        qp.setPen(QColor(128, 128, 128))
        xs = range(d, w, d)
        vs = [Central.V(x, 0) for x in xs]
        v_min, v_max = min(*vs), max(*vs)
        k = 255 / (v_max - v_min)
        ns = [(v - v_min) * k for v in vs]
        ps = [QPoint(x, n) for x, n in zip(xs, ns)]
        qp.drawPolyline(*ps)

        qp.end()


# ========================================== Main

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Movie()
    sys.exit(app.exec_())
