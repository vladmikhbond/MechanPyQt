from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QPixmap, QImage
from PyQt5.QtCore import QPoint, Qt

TRACK_COLOR = QColor('red')
BALL_COLOR = QColor('red')
SUN_COLOR = QColor('yellow')
V_PROF_COLOR = QColor('white')

class FieldWidget(QWidget):

    def __init__(self, parent, model):
        super().__init__(parent)
        self.model = model
        self.fieldImage = None
        self.ballImage = QImage()
        self.ballImage.load('ui/ball.png')

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        if self.fieldImage:
            qp.drawPixmap(0, 0, self.fieldImage)

        # balls
        qp.translate(self.model.width / 2, self.model.height / 2)
        qp.scale(1, -1)
        qp.setPen(BALL_COLOR)
        r = 11
        for b in self.model.balls:
            qp.drawImage(QPoint(b.x-r, b.y-r), self.ballImage)

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
        # qp = QPainter()
        # qp.begin(pix)
        # qp.translate(self.model.width / 2, self.model.height / 2)
        # qp.scale(1, -1)
        #
        # w = self.model.width // 2
        # d = self.model.cell
        # k = self.model.K
        # if k != 0:
        #     qp.setPen(V_PROF_COLOR)
        #     xs = range(d, w, d)
        #     vs = [Central.V(x, 0) * k for x in xs]
        #     ps = [QPoint(x, v) for x, v in zip(xs, vs)]
        #     qp.drawPolyline(*ps)
        # qp.end()

        self.fieldImage = pix
