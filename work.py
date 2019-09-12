import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QTimer, QPoint
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
        self.ball = Ball(50, 50, 1, 1)


    def step(self):
        self.ball.fx = 0;
        self.ball.fy = 0.01;
        self.ball.step()
        self.repaint()


    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)

        qp.setPen(QColor(168, 34, 3))
        b = self.ball
        qp.drawEllipse(QPoint(b.x,b.y),30,30)

        qp.end()



    # def drawText(self, event, qp):
    #     qp.setPen(QColor(168, 34, 3))
    #     qp.setFont(QFont('Decorative', 10))
    #     qp.drawText(event.rect(), Qt.AlignCenter, self.x)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


