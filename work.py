import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import QTimer, QPoint
from Ball import Ball
from Central import Central
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
        self.central = Central(800, 800, Ball(100, 0, 0, 10))


        self.ui.okButton.clicked.connect(self.okBtnClicked)
        self.okBtnClicked()

    def step(self):
        self.central.step()
        self.repaint()

    def paintEvent(self, event):
        qp = QPainter()

        qp.begin(self)
        qp.translate(self.central.width / 2, self.central.height / 2)
        qp.scale(1, -1)
        # draw Center
        qp.drawEllipse(QPoint(0, 0), 5, 5)

        self.drawBalls(qp)
        qp.end()

    def drawBalls(self, qp):
        qp.setBrush(QColor(168, 34, 3))
        r = 10
        for b in self.central.balls:
            qp.drawEllipse(QPoint(b.x, b.y), r, r)
            for p in b.points:
                qp.drawPoint(p)


    def okBtnClicked(self):
        text = self.ui.potential.toPlainText()
        self.central.refresh(text)


        text = self.ui.conditions.toPlainText()
        self.central.balls[0].refresh(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Movy()
    sys.exit(app.exec_())
