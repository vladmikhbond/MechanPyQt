import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QTimer, QRect
from model.Ball import Ball
from model.Central import Central
from ui.mainForm import Ui_MainWindow  # импорт нашего сгенерированного файла
from fieldWidget import FieldWidget


T_INTERVAL = 20


class Main(QMainWindow):

    def __init__(self):
        super().__init__()

        # init model
        self.model = Central(800, 800, Ball())

        # init UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.fieldWidget = FieldWidget(self, self.model)
        self.fieldWidget.setGeometry(QRect(10, 110, self.model.width, self.model.height))
        self.fieldWidget.setMouseTracking(True)
        self.fieldWidget.setObjectName("fieldWidget")
        self.show()

        # init timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.step)

        # init handlers
        self.setMouseTracking(True)
        self.ui.okButton.clicked.connect(self.okBtnClicked)

        # first time drawing
        self.okBtnClicked()

    # ========================================== Handlers

    def mousePressEvent(self, event):
        # diagnostic print
        p = self.model.ScreenToWorld(event.pos())
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
        if self.model.refresh(text):
            self.fieldWidget.createFieldImage()
        else:
            print("ERROR")

        # renew a ball
        text = self.ui.conditions.toPlainText()
        self.model.balls[0].refresh(text)
        self.timer.start(T_INTERVAL)

    def step(self):
        # stop timer when a ball is far away
        if self.model.balls[0].r() > self.model.width * 2:
            self.timer.stop()

        # many steps and one painting
        for i in range(10):
            self.model.step()

        self.fieldWidget.repaint()

        # energy diagnostic
        b = self.model.balls[0];
        o = b.lagrangian()
        self.setWindowTitle(f'E = { b.T() + b.V() :12.8f}   L = {o[0] + o[1]  :12.8f}, {o[2] + o[3]  :12.8f}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())
