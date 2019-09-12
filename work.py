import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import QTimer, QPoint
from Ball import Ball
from ui.mainForm import Ui_MainWindow  # импорт нашего сгенерированного файла


class Example(QMainWindow):

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
        self.ball = Ball(x=100, y=0, vx=0, vy=1)

        self.ui.okButton.clicked.connect(self.okBtnClicked)

    def step(self):
        k = -10000
        b = self.ball
        r2 = (b.x**2 + b.y**2)**2
        b.fx = k * b.x / r2
        b.fy = k * b.y / r2
        b.step()
        self.repaint()

    def paintEvent(self, event):
        qp = QPainter()

        qp.begin(self)
        qp.translate(400, 400)
        qp.scale(1, -1)
        # draw Center
        qp.drawEllipse(QPoint(0, 0), 5, 5)
        qp.drawPoint(QPoint(0, 0))

        # draw ball
        qp.setBrush(QColor(168, 34, 3))
        b = self.ball
        r = 10
        qp.drawEllipse(QPoint(b.x, b.y), r, r)

        qp.end()

    def okBtnClicked(self):
        text = self.ui.textEdit.toPlainText()
        o = eval(text)
        self.ball.x = o['x']
        self.ball.y = o['y']


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
