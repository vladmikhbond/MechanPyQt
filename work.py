import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QPainter, QColor, QPolygon
from PyQt5.QtCore import QTimer, QPoint
from Ball import Ball
from ui.mainForm import Ui_MainWindow  # импорт нашего сгенерированного файла

class Movy(QMainWindow):

    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.show()
        ###
        self.timer = QTimer()
        self.timer.timeout.connect(self.step)
        self.timer.start(10)
        ##########################################################
        self.ball = Ball(x=100, y=0, vx=0, vy=10)

        self.ui.okButton.clicked.connect(self.okBtnClicked)
        self.okBtnClicked()

    def step(self):
        k = -0.01
        b = self.ball

        b.fx = k * b.x
        b.fy = k * b.y

        d = 0.01
        b.fx = (self.V(b.x + d, b.y) - self.V(b.x - d, b.y)) / (2 * d)
        b.fy = (self.V(b.x, b.y + d) - self.V(b.x, b.y - d)) / (2 * d)


        b.step()
        self.repaint()

    def paintEvent(self, event):
        qp = QPainter()

        qp.begin(self)
        qp.translate(400, 400)
        qp.scale(1, -1)
        # draw Center
        qp.drawEllipse(QPoint(0, 0), 5, 5)

        Movy.drawBall(qp, self.ball)
        qp.end()

    @staticmethod
    def drawBall(qp, b):
        qp.setBrush(QColor(168, 34, 3))
        r = 10
        qp.drawEllipse(QPoint(b.x, b.y), r, r)
        for p in b.points:
            qp.drawPoint(p)


    def okBtnClicked(self):
        text = self.ui.textEdit.toPlainText()
        self.V = eval("lambda x, y: " + text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Movy()
    sys.exit(app.exec_())
