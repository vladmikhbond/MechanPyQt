import sys
from model.Settings import settings as ss

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QTimer, QRect, QPoint
from model.Ball import Ball
from model.Central import Central
from ui.mainForm import Ui_MainWindow  # импорт нашего сгенерированного файла
from fieldWidget import FieldWidget
from glWidget import GLWidget


FIELD_SIDE = 700
T_INTERVAL = 20

class Main(QMainWindow):

    def __init__(self):
        super().__init__()

        # init model
        self.model = Central(FIELD_SIDE, ss.cell, Ball())

        # init UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.glWidget = GLWidget(self, self.model, ss)
        self.glWidget.setGeometry(QRect(10, 150, self.model.width, self.model.height))
        self.glWidget.setObjectName("glWidget")

        self.fieldWidget = FieldWidget(self, self.model)
        self.fieldWidget.setGeometry(QRect(10, 150, self.model.width, self.model.height))
        self.fieldWidget.setMouseTracking(True)
        self.fieldWidget.setObjectName("fieldWidget")
        #
        self.ui.settings.setPlainText(ss.paramsToStr())
        self.ui.potential.setPlainText(ss.V)
        self.ui.conditions.setPlainText(ss.ballToStr())

        self.show()


        # init handlers
        self.setMouseTracking(True)
        self.ui.okButton.clicked.connect(self.okBtnClicked)
        self.ui.okBallButton.clicked.connect(self.okBallBtnClicked)
        self.ui.viewSlider.valueChanged.connect(self.viewSlider_changed)

        # first time drawing
        self.resetSettings()

        # init timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.step)
        self.timerStart()


    # ========================================== Settings

    def timerStart(self):
        # if ss.view:
        #     self.fieldWidget.setVisible(False)
        #     self.timer.stop()
        # else:
        self.fieldWidget.setVisible(True)
        self.timer.start(T_INTERVAL)

    # ========================================== Handlers
    def viewSlider_changed(self):
        val = self.ui.viewSlider.value()
        ss.view = val
        self._changeSettingsText(val, "view=", " ")

        val = -abs(val + 7)
        self.glWidget.light = val
        self._changeSettingsText(val, "light=", ",")

        self.glWidget.repaint()

    def _changeSettingsText(self, val, key1, key2):
        text = self.ui.settings.toPlainText()
        idx1 = text.find(key1) + len(key1)
        idx2 = text.find(key2, idx1)
        if idx2 == -1:
            idx2 = len(text)
        self.ui.settings.setPlainText(text[:idx1] + str(val) + text[idx2:])


    def mousePressEvent(self, event):
        # diagnostic print
        p = self.screenToWorld(event.pos())
        v = Central.V(p.x(), p.y())
        z = self.glWidget.z(p.x(), p.y())
        print(f'x={p.x():4}  y={p.y():4}  v={v:0.4f}  z={z:0.4f}')

        # toggle timer
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timerStart()

    def screenToWorld(self, cur: QPoint):
        x0, y0 = self.model.width / 2, self.model.height / 2
        x = cur.x() - self.fieldWidget.geometry().x()
        y = cur.y() - self.fieldWidget.geometry().y()
        return QPoint(x - x0, y0 - y )

    def okBtnClicked(self):
        self.resetSettings()
        self.timerStart()
        self.glWidget.repaint()

    def okBallBtnClicked(self):
        self.resetSettings()
        self.timerStart()

    # from input text
    #
    def resetSettings(self):
        ss.reset(self.ui.settings.toPlainText(),
                 self.ui.potential.toPlainText(),
                 self.ui.conditions.toPlainText())
        self.model.reset(ss)
        self.fieldWidget.createFieldImage()
        # correct slider positions
        self.ui.viewSlider.setValue(ss.view)
        #
        self.model.balls[0].setEo()

    def step(self):
        # stop timer when a ball is far away
        if self.model.balls[0].r() > self.model.width * 2:
            self.timer.stop()

        # many steps and one painting
        for i in range(10):
            self.model.step()

        self.fieldWidget.repaint()

        # diagnostic: Energy and Lagrangian
        b = self.model.balls[0]
        self.setWindowTitle(f' E = {b.Eo:12.8f}    gap = {b.gap():12.8f}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())
