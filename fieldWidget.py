from PyQt5.QtWidgets import QWidget
from model.Central import Central
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QPixmap
from PyQt5.QtCore import QPoint, Qt

TRACK_COLOR = QColor('red')
BALL_COLOR = QColor('red')
SUN_COLOR = QColor('yellow')
V_PROF_COLOR = QColor(128, 128, 128)

class FieldWidget(QWidget):

    def __init__(self, parent, model):
        super().__init__(parent)
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
            if b.drawX:
                qpi.drawLine(b.x, b.y, b.drawX, b.drawY)
            b.drawX = b.x
            b.drawY = b.y

        qpi.end()

    def createFieldImage(self):
        pix = QPixmap(self.model.width, self.model.height)
        pix.fill(Qt.transparent)

        # draw V-profile
        qp = QPainter()
        qp.begin(pix)
        qp.translate(self.model.width / 2, self.model.height / 2)
        qp.scale(1, -1)

        w = self.model.width // 2
        d = self.model.cell
        qp.setPen(V_PROF_COLOR)
        xs = range(d, w, d)
        vs = [Central.V(x, 0) for x in xs]
        v_min, v_max = min(*vs), max(*vs)
        if v_max != v_min:
            k = 255 / (v_max - v_min)
            ns = [(v - v_min) * k for v in vs]
            ps = [QPoint(x, n) for x, n in zip(xs, ns)]
            qp.drawPolyline(*ps)
        qp.end()

        self.fieldImage = pix
