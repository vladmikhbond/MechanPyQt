from PyQt5.QtWidgets import QWidget
from model.Central import Central
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QPixmap
from PyQt5.QtCore import QPoint

TRACK_COLOR = QColor('red')
BALL_COLOR = QColor('red')
SUN_COLOR = QColor('yellow')
V_PROF_COLOR = QColor(128, 128, 128)

class FieldWidget(QWidget):

    def __init__(self, owner, model):
        super().__init__(owner)
        self.model = model
        self.fieldImage = None

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        if self.fieldImage:
            qp.drawPixmap(0, 0, self.fieldImage)

        # balls
        qp.translate(self.model.width / 2, self.model.height / 2)
        qp.scale(1, -1)
        qp.setPen(BALL_COLOR)
        qp.setBrush(BALL_COLOR)
        r = 10
        for b in self.model.balls:
            qp.drawEllipse(QPoint(b.x, b.y), r, r)
        qp.end()

        # tracks to image
        qpi = QPainter()
        qpi.begin(self.fieldImage)
        qpi.translate(self.model.width / 2, self.model.height / 2)
        qpi.scale(1, -1)
        qpi.setPen(TRACK_COLOR)
        for b in self.model.balls:
            if b.prevX:
                qpi.drawLine(b.x, b.y, b.prevX, b.prevY)
            b.prevX = b.x
            b.prevY = b.y

        qpi.end()

    def createFieldImage(self):
        self.fieldImage = QPixmap(self.model.width, self.model.height)
        qp = QPainter()
        qp.begin(self.fieldImage)
        qp.translate(self.model.width / 2, self.model.height / 2)
        qp.scale(1, -1)

        w = self.model.width // 2
        h = self.model.height // 2
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

        # draw center
        qp.setPen(QPen(QBrush(BALL_COLOR), 1))
        qp.setBrush(SUN_COLOR)
        qp.drawEllipse(QPoint(0, 0), 5, 5)

        # draw V-profile
        qp.setPen(V_PROF_COLOR)
        xs = range(d, w, d)
        vs = [Central.V(x, 0) for x in xs]
        v_min, v_max = min(*vs), max(*vs)
        k = 255 / (v_max - v_min)
        ns = [(v - v_min) * k for v in vs]
        ps = [QPoint(x, n) for x, n in zip(xs, ns)]
        qp.drawPolyline(*ps)

        qp.end()
