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
        MainWindow.resize(836, 936)
        font = QtGui.QFont()
        font.setPointSize(15)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(10, 10, 801, 91))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.frame.setFont(font)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(19, 15, 41, 21))
        self.label.setObjectName("label")
        self.potential = QtWidgets.QTextEdit(self.frame)
        self.potential.setGeometry(QtCore.QRect(70, 10, 641, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.potential.setFont(font)
        self.potential.setDocumentTitle("")
        self.potential.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Courier New\'; font-size:12pt; font-style:italic; color:#808080;\">0.00005 * (x*x + y*y)</span></p></body></html>")
        self.potential.setAcceptRichText(False)
        self.potential.setPlaceholderText("")
        self.potential.setObjectName("potential")
        self.okButton = QtWidgets.QPushButton(self.frame)
        self.okButton.setGeometry(QtCore.QRect(720, 10, 71, 71))
        self.okButton.setObjectName("okButton")
        self.conditions = QtWidgets.QTextEdit(self.frame)
        self.conditions.setGeometry(QtCore.QRect(70, 50, 641, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.conditions.setFont(font)
        self.conditions.setDocumentTitle("")
        self.conditions.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Courier New\'; font-size:12pt; font-style:italic; color:#808080;\">\'x\': 100, \'y\': 0,  \'vx\': 0,  \'vy\': 1 </span></p></body></html>")
        self.conditions.setAcceptRichText(False)
        self.conditions.setPlaceholderText("")
        self.conditions.setObjectName("conditions")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(20, 50, 41, 21))
        self.label_2.setObjectName("label_2")
        # self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        # self.scrollArea.setGeometry(QtCore.QRect(10, 120, 821, 721))
        # self.scrollArea.setStyleSheet("background-color: rgb(15, 255, 23);")
        # self.scrollArea.setWidgetResizable(True)
        # self.scrollArea.setObjectName("scrollArea")
        # self.scrollAreaWidgetContents = QtWidgets.QWidget()
        # self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 819, 719))
        # self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        # self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 836, 18))
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
        self.label.setText(_translate("MainWindow", "V = "))
        self.okButton.setText(_translate("MainWindow", "Ok"))
        self.label_2.setText(_translate("MainWindow", "00 = "))
