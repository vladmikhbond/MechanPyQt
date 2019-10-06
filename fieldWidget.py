import math
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QPixmap, QImage
from PyQt5.QtCore import QPoint, QRectF, Qt
from model.Setting import setting as ss

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
        w, h = self.model.width / 2, self.model.height / 2
        qp = QPainter()
        qp.setPen(BALL_COLOR)
        y_scale = math.cos(ss.view * math.pi / 180)

        qp.begin(self)
        qp.translate(w, h)

        qp.save()


        # back image

        qp.scale(1, y_scale)
        if self.fieldImage:
            qp.drawPixmap(-w, -h, self.fieldImage)
        qp.restore()

        # just ball
        qp.scale(1, -y_scale)
        r = 11
        for b in self.model.balls:
            qp.drawImage(QPoint(b.x-r, b.y-r), self.ballImage)

        qp.end()

        # put tracks to image
        qpi = QPainter()
        qpi.begin(self.fieldImage)
        qpi.translate(w, h)
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
        self.fieldImage = pix
