# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\mainForm.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(721, 905)
        font = QtGui.QFont()
        font.setPointSize(15)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(10, 10, 701, 131))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.frame.setFont(font)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.potential = QtWidgets.QPlainTextEdit(self.frame)
        self.potential.setGeometry(QtCore.QRect(10, 50, 601, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.potential.setFont(font)
        self.potential.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.potential.setObjectName("potential")
        self.okButton = QtWidgets.QPushButton(self.frame)
        self.okButton.setGeometry(QtCore.QRect(620, 10, 71, 71))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.okButton.setFont(font)
        self.okButton.setObjectName("okButton")
        self.conditions = QtWidgets.QPlainTextEdit(self.frame)
        self.conditions.setGeometry(QtCore.QRect(10, 90, 601, 31))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(9)
        font.setItalic(False)
        self.conditions.setFont(font)
        self.conditions.setStyleSheet("")
        self.conditions.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.conditions.setObjectName("conditions")
        self.settings = QtWidgets.QPlainTextEdit(self.frame)
        self.settings.setGeometry(QtCore.QRect(10, 10, 601, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.settings.setFont(font)
        self.settings.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.settings.setObjectName("settings")
        self.okBallButton = QtWidgets.QPushButton(self.frame)
        self.okBallButton.setGeometry(QtCore.QRect(620, 90, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.okBallButton.setFont(font)
        self.okBallButton.setObjectName("okBallButton")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(10, 150, 700, 700))
        self.scrollArea.setStyleSheet("background-color: rgb(15, 255, 23);")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 698, 698))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.comment = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.comment.setGeometry(QtCore.QRect(10, 860, 701, 91))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.comment.setFont(font)
        self.comment.setObjectName("comment")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 721, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.potential.setToolTip(_translate("MainWindow", "Potential Energy"))
        self.potential.setPlainText(_translate("MainWindow", "0.00005 * r**2"))
        self.okButton.setText(_translate("MainWindow", "Ok"))
        self.conditions.setToolTip(_translate("MainWindow", "Initial Conditions"))
        self.conditions.setPlainText(_translate("MainWindow", "\'x\':100, \'y\':0, \'vx\':0, \'vy\':1 "))
        self.settings.setToolTip(_translate("MainWindow", "Settings"))
        self.settings.setPlainText(_translate("MainWindow", "\'kz\': 1"))
        self.okBallButton.setText(_translate("MainWindow", "Ok"))
        self.comment.setPlainText(_translate("MainWindow", "0.00005 * r**2    - резиновая нить, есть круговые орбиты, их частота одинакова\n"
"0.01 * r         - сила не зависит от расстояния, есть круговые орбиты\n"
"-100 / r       - потенциал поля тяготения (сила обратно пропорц. квадрату расстояния)\n"
"-5000 / r**2 - сила обратно пропорц. кубу расстояния - неуст.орбиты\n"
"\n"
"100 *  math.sin(r/ 20) \n"
"\n"
"10 *  math.sin((x - y)/ 50) - (Нецентральные) полет по синусоиде\n"
"math.log(r)\n"
""))
