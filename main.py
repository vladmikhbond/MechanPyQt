import sys
from model.Setting import setting as se
from model.Archive import archive


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
        self.model = Central(FIELD_SIDE, se.cell, Ball())

        # init UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # glWidget
        self.glWidget = GLWidget(self, self.model, se)
        self.glWidget.setGeometry(QRect(10, 150, self.model.width, self.model.height))
        self.glWidget.setObjectName("glWidget")
        # fieldWidget
        self.fieldWidget = FieldWidget(self, self.model)
        self.fieldWidget.setGeometry(QRect(10, 150, self.model.width, self.model.height))
        self.fieldWidget.setMouseTracking(True)
        self.fieldWidget.setObjectName("fieldWidget")
        # text fields
        self.ui.settings.setPlainText(se.paramsToStr())
        self.ui.potential.setPlainText(se.V)
        self.ui.conditions.setPlainText(se.ballToStr())
        # fill arcList
        items = [a.getComment() for a in archive]
        self.ui.arcList.addItems(items)

        self.show()

        # init handlers
        self.setMouseTracking(True)
        self.ui.okButton.clicked.connect(self.okBtn_clicked)
        self.ui.okBallButton.clicked.connect(self.okBallBtn_clicked)
        self.ui.viewSlider.valueChanged.connect(self.viewSlider_changed)
        self.ui.arcList.itemSelectionChanged.connect(self.arc_selected)
        self.ui.arcAddButton.clicked.connect(self.arcAddButton_clicked)
        self.ui.arcRemButton.clicked.connect(self.arcRemButton_clicked)

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
    def arc_selected(self):
        i = self.ui.arcList.currentRow()
        if i > -1:
            setting = archive[i]
            self.ui.settings.setPlainText(setting.paramsToStr())
            self.ui.potential.setPlainText(setting.V)
            self.ui.conditions.setPlainText(setting.ballToStr())

    def arcRemButton_clicked(self):
        lst = self.ui.arcList
        i = lst.currentRow()
        if i == -1: return
        archive.pop(i)
        archive.saveToFile()
        # ui
        lst.removeItemWidget(lst.takeItem(i))

    def arcAddButton_clicked(self):
        archive.addSetting(se)
        archive.saveToFile()
        # ui
        self.ui.arcList.insertItem(0, se.getComment())

    def viewSlider_changed(self):
        val = self.ui.viewSlider.value()
        se.view = val
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

    def okBtn_clicked(self):
        self.resetSettings()
        self.timerStart()
        self.glWidget.repaint()

    def okBallBtn_clicked(self):
        self.resetSettings()
        self.timerStart()

    # from input text
    #
    def resetSettings(self):
        se.reset(self.ui.settings.toPlainText(),
                 self.ui.potential.toPlainText(),
                 self.ui.conditions.toPlainText())
        self.model.reset(se)
        self.fieldWidget.createFieldImage()
        # correct slider positions
        self.ui.viewSlider.setValue(se.view)
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
