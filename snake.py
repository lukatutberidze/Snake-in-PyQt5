from pynput.keyboard import Key, Listener
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import threading
import time
import random

closed=False
class Ui_MainWindow(QObject):
    updater=QtCore.pyqtSignal()
    def __init__(self):
            super().__init__()
            self.updater.connect(self.update)
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 640)
        MainWindow.setStyleSheet("background-color: rgb(66, 66, 66);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.head = QtWidgets.QLabel(self.centralwidget)
        self.head.setGeometry(QtCore.QRect(360, 240, 20, 20))
        self.head.setStyleSheet("background-color: rgb(0, 170, 0);")
        self.head.setText("")
        self.head.setObjectName("label")
        self.fx,self.fy=random.randint(0,40)*20,random.randint(0,30)*20
        self.xinkali = QtWidgets.QLabel(self.centralwidget)
        self.xinkali.setGeometry(QtCore.QRect(self.fx, self.fy, 20, 20))
        self.xinkali.setStyleSheet("background-color: rgb(255, 57, 39);")
        self.xinkali.setText("")
        self.xinkali.setObjectName("xinkali")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.setup()

    def setup(self):
        self.ls=[[self.head,'r',360,240]]
        a=threading.Thread(target=self.move)
        a.start()
        b=threading.Thread(target=self.snupdate)
        b.start()

    def move(self):
        def on_press(key):
            check_key(key)
        def check_key(key):
            if key==Key.up and self.ls[0][1]!='d': 
                self.ls[0][1]='u'
            elif key==key.down and self.ls[0][1]!='u':
                self.ls[0][1]='d'
            elif key==key.left and self.ls[0][1]!='r':
                self.ls[0][1]='l'
            elif key==key.right and self.ls[0][1]!='l':
                self.ls[0][1]='r'
        with Listener(on_press=on_press) as listener:listener.join()

    def update(self):
        l=[[i[2],i[3]] for i in self.ls]
        for i in l:
            if l.count(i)>1:
                for i in self.ls[1:]:
                    i[0].hide()
                self.ls=[self.ls[0]]
        for i in range(len(self.ls)):
            if self.ls[i][2]==-20:
                self.ls[i][2]=780
            elif self.ls[i][2]==800:
                self.ls[i][2]=0
            elif self.ls[i][3]==-20:
                self.ls[i][3]=600
            elif self.ls[i][3]==620:
                self.ls[i][3]=0
            if self.ls[0][2]==self.fx and self.ls[0][3]==self.fy:
                self.fx,self.fy=random.randint(0,39)*20,random.randint(0,29)*20
                while [self.fx,self.fy] in l:
                    self.fx,self.fy=random.randint(0,39)*20,random.randint(0,29)*20
                self.xinkali.setGeometry(QtCore.QRect(self.fx, self.fy, 20, 20))
                self.body=QtWidgets.QLabel(self.centralwidget)
                a,b=self.ls[-1][2],self.ls[-1][3]
                if self.ls[-1][1]=='u':
                    b+=20
                elif self.ls[-1][1]=='d':
                    b-=20
                elif self.ls[-1][1]=='r':
                    a-=20
                else:
                    a+=20
                self.body.setGeometry(QtCore.QRect(a, b, 20, 20))
                self.body.show()
                self.body.setStyleSheet("background-color: rgb(0, 170, 0);")
                self.ls.append([self.body,self.ls[-1][1],a,b])
            self.ls[i][0].setGeometry(QtCore.QRect(self.ls[i][2], self.ls[i][3], 20, 20))
    def snupdate(self):
        while True:
            time.sleep(0.05)
            if len(self.ls)>1:
                self.ls[-1][0].hide()
                x=self.ls[-1][0]
                self.ls=self.ls[:-1]
                a,b=self.ls[0][2],self.ls[0][3]
                if self.ls[0][1]=='u':
                    b-=20
                elif self.ls[0][1]=='d':
                    b+=20
                elif self.ls[0][1]=='r':
                    a+=20
                else:
                    a-=20
                self.ls.insert(0,[x,self.ls[0][1],a,b])
                self.ls[0][0].show()
            if len(self.ls)==1:
                for i in range(len(self.ls)):
                    if self.ls[i][1]=='u':
                        self.ls[i][3]-=20
                    elif self.ls[i][1]=='d':
                        self.ls[i][3]+=20
                    elif self.ls[i][1]=='r':
                        self.ls[i][2]+=20
                    else:
                        self.ls[i][2]-=20
            self.updater.emit()
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Snake by luka"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())