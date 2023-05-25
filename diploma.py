# -*- coding: utf-8 -*-
import easygui as eg
from PyQt5 import QtCore, QtGui, QtWidgets
import datetime as dt
import funcs
import os
import subprocess
from datetime import datetime


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(688, 388)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton.setGeometry(QtCore.QRect(10, 10, 111, 31))
        self.toolButton.setObjectName("toolButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(130, 10, 121, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(570, 50, 81, 21))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(260, 10, 111, 31))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(40, 320, 91, 23))
        self.pushButton_5.setObjectName("pushButton_5")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 121, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(170, 80, 501, 271))
        self.label_3.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label_3.setFrameShape(QtWidgets.QFrame.Box)
        self.label_3.setText("")
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(170, 50, 121, 16))
        self.label_4.setObjectName("label_4")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(380, 20, 271, 21))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem('')
        self.comboBox.addItem('Абсолютный метод')
        self.comboBox.addItem('Относительный метод')
        self.comboBox.addItem('Относительный метод + PPP')
        self.comboBox.addItem('PPP метод')
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 80, 151, 231))
        self.listWidget.setFrameShape(QtWidgets.QFrame.Box)
        self.listWidget.setFrameShadow(QtWidgets.QFrame.Plain)
        self.listWidget.setObjectName("listWidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(380, 0, 201, 16))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 688, 21))
        self.menuBar.setObjectName("menuBar")
        self.menu = QtWidgets.QMenu(self.menuBar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menuBar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menuBar)
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.action_3 = QtWidgets.QAction(MainWindow)
        self.action_3.setObjectName("action_3")
        self.action_4 = QtWidgets.QAction(MainWindow)
        self.action_4.setObjectName("action_4")
        self.menu.addAction(self.action_3)
        self.menu_2.addAction(self.action_4)
        self.menuBar.addAction(self.menu.menuAction())
        self.menuBar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.functions()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RINEX Post Processing"))
        self.toolButton.setText(_translate("MainWindow", "Выбрать файл"))
        self.pushButton_2.setText(_translate("MainWindow", "Конвертер TPS2RNX"))
        self.pushButton_3.setText(_translate("MainWindow", "Старт"))
        self.pushButton_4.setText(_translate("MainWindow", "Выгрузить данные"))
        self.pushButton_5.setText(_translate("MainWindow", "Удалить файл"))
        self.label_2.setText(_translate("MainWindow", "Список файлов:"))
        self.label_4.setText(_translate("MainWindow", "Итоги обработки:"))
        self.label.setText(_translate("MainWindow", "Выберите тип пост-обработки:"))
        self.menu.setTitle(_translate("MainWindow", "Меню"))
        self.menu_2.setTitle(_translate("MainWindow", "Помощь"))
        self.action.setText(_translate("MainWindow", "Сохранить"))
        self.action_3.setText(_translate("MainWindow", "Закрыть"))
        self.action_4.setText(_translate("MainWindow", "Справка"))

    def functions(self):
        self.toolButton.clicked.connect(self.filesprov)
        self.pushButton_5.clicked.connect(self.delfile)
        self.pushButton_3.clicked.connect(self.startpost)
        self.pushButton_2.clicked.connect(self.convert)
        self.pushButton_4.clicked.connect(self.save)
        self.action_3.triggered.connect(self.exit)
        self.action_4.triggered.connect(self.help)
    def help(self):
        helptxt = 'Справка.txt'
        subprocess.Popen(['C:\\Windows\\System32\\notepad.exe', helptxt])
    def exit(self):
        sys.exit(app.exec_())
    def save(self):
        path = eg.diropenbox()
        print(path)
        filename = path + '\RINEXPostProcessing.txt'
        savetxt = open(filename, 'w+')
        savetxt.write(self.label_3.text())
        savetxt.close()
    def convert(self):
        qo = eg.fileopenbox()
        converter = os.path.abspath('tps2rin.exe')
        subprocess.Popen([converter, qo])
    def filesprov(self):
        qo = eg.fileopenbox()
        self.listWidget.addItem(qo)
    def delfile(self):
        qn = self.listWidget.currentRow()
        self.listWidget.takeItem(qn)
    def startpost(self):
        items = []
        ob = 0
        for index in range(self.listWidget.count()):
            if self.listWidget.item(index).text().endswith('o'):
                ob += 1
            items.append(self.listWidget.item(index).text())
        if ob == 0:
            self.label_3.setText('Добавьте файл наблюдений (.**o')
            return
        elif ob >= 2:
            self.label_3.setText('Оставьте один файл наблюдений (.**o')
            return
        else:
            pass
        n = 0
        for lines in range(len(items)):
            if items[lines].endswith('o'):
                obsfile = items[lines]
            elif items[lines].endswith('sp3'):
                sp3file = items[lines]
            elif items[lines].endswith('clk'):
                clkfile = items[lines]
            else:
                n += 1
                navfile = items[lines]
        if n == 0:
            self.label_3.setText('Добавьте файл навигационного сообщения')
            return
        elif n >= 2:
            self.label_3.setText('Оставьте один файл навигационного сообщения')
            return
        else:
            pass
        if self.comboBox.currentText() == 'Абсолютный метод':
            obs = funcs.readfile(obsfile)
            nav = funcs.readfile(navfile)
            compile = funcs.compile2(nav[5], obs[10], obs[5])
            Xtrue, Ytrue, Ztrue, coor, fi, lu = funcs.absolute(compile)
            typeobs = obs[0]
            first_obs = dt.datetime(year = obs[3][0], month = obs[3][1], day = obs[3][2],
                                    hour = obs[3][3], minute = obs[3][4], second = int(obs[3][5]))
            chas = obs[5]

            text = 'Тип файла (смешанные наблюдения или нет): ' + str(typeobs) + ' \n' + 'Дата и время первого наблюдения: ' + str(first_obs) + ' \n' + 'Частоты, по ' \
                'которым производились измерения: ' + '\n' + str(chas) + ' \n' + 'Декартовые координаты приемника: '+ '\n' + str(Xtrue) + ', ' + str(Ytrue) + ', ' + str(Ztrue) + ' \n' + 'Геодезические' \
                 ' координаты (в WGS 84): '+ '\n' + str(fi) + ' широты, ' + str(lu) + ' долготы'
            self.label_3.setText(text)
        elif self.comboBox.currentText() == 'Относительный метод':
            obs = funcs.readfile(obsfile)
            nav = funcs.readfile(navfile)
            compile = funcs.compile2(nav[5], obs[10], obs[5])
            Xtrue, Ytrue, Ztrue, coor, fi, lu = funcs.absolute(compile)
            typeobs = obs[0]
            first_obs = dt.datetime(year=obs[3][0], month=obs[3][1], day=obs[3][2],
                                    hour=obs[3][3], minute=obs[3][4], second=int(obs[3][5]))
            chas = obs[5]

            text = 'Тип файла (смешанные наблюдения или нет): ' + str(typeobs) + ' \n' + 'Дата и время первого наблюдения: ' + str(first_obs) + ' \n' + 'Частоты, по ' \
                'которым производились измерения: ' + '\n' + str(chas) + ' \n' + 'Декартовые координаты приемника: '+ '\n' + str(Xtrue) + ', ' + str(Ytrue) + ', ' + str(Ztrue) + ' \n' + 'Геодезические' \
                 ' координаты (в WGS 84): '+ '\n' + str(fi) + ' широты, ' + str(lu) + ' долготы'
            self.label_3.setText(text)
        elif self.comboBox.currentText() == 'Относительный метод + PPP':
            obs = funcs.readfile(obsfile)
            nav = funcs.readfile(navfile)
            compile = funcs.compile2(nav[5], obs[10], obs[5])
            Xtrue, Ytrue, Ztrue, coor, fi, lu = funcs.absolute(compile)
            typeobs = obs[0]
            first_obs = dt.datetime(year=obs[3][0], month=obs[3][1], day=obs[3][2],
                                    hour=obs[3][3], minute=obs[3][4], second=int(obs[3][5]))
            chas = obs[5]

            text = 'Тип файла (смешанные наблюдения или нет): ' + str(typeobs) + ' \n' + 'Дата и время первого наблюдения: ' + str(first_obs) + ' \n' + 'Частоты, по ' \
                'которым производились измерения: ' + '\n' + str(chas) + ' \n' + 'Декартовые координаты приемника: '+ '\n' + str(Xtrue) + ', ' + str(Ytrue) + ', ' + str(Ztrue) + ' \n' + 'Геодезические' \
                 ' координаты (в WGS 84): '+ '\n' + str(fi) + ' широты, ' + str(lu) + ' долготы'
            self.label_3.setText(text)
        elif self.comboBox.currentText() == 'PPP метод':
            obs = funcs.readfile(obsfile)
            nav = funcs.readfile(navfile)
            compile = funcs.compile2(nav[5], obs[10], obs[5])
            Xtrue, Ytrue, Ztrue, coor, fi, lu = funcs.absolute(compile)
            typeobs = obs[0]
            first_obs = dt.datetime(year=obs[3][0], month=obs[3][1], day=obs[3][2],
                                    hour=obs[3][3], minute=obs[3][4], second=int(obs[3][5]))
            chas = obs[5]

            text = 'Тип файла (смешанные наблюдения или нет): ' + str(typeobs) + ' \n' + 'Дата и время первого наблюдения: ' + str(first_obs) + ' \n' + 'Частоты, по ' \
                'которым производились измерения: ' + '\n' + str(chas) + ' \n' + 'Декартовые координаты приемника: '+ '\n' + str(Xtrue) + ', ' + str(Ytrue) + ', ' + str(Ztrue) + ' \n' + 'Геодезические' \
                 ' координаты (в WGS 84): '+ '\n' + str(fi) + ' широты, ' + str(lu) + ' долготы'
            self.label_3.setText(text)
        else:
            pass
        #ads = self.listWidget.123
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())