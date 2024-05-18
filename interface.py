import serial.tools.list_ports
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtCore, QtGui, QtWidgets
from handlers import convert_input_data
import json


isFileOpened = False
"""
Функция считывает данные из серийного порта, 
если он открыт, и декодирует их
"""


def handle_available_data(self, file):
    global isFileOpened
    if self.serialInst.isOpen():
        packet = self.serialInst.readline()
        data =packet.decode('ascii', errors='ignore').rstrip('\n')
        data = data.strip('\r')
        print(data)
        arr = convert_input_data(chart, data)
        data = {}
        #data[self.label_2.text()] = {}
        #gestures = data[self.label_2.text()]
        #if isFileOpened:
        #    if data[self.label_2.text()] == {} or gestures['Жесты']['index'] != self.label_3:
        #        data[self.label_2.text()] = {}
        #        gestures = data[self.label_2.text()]
        #        gestures['Жесты'] = []
        #        gestures['Жесты'].append({
        #            'name': 'жест',
        #            'index': self.label_3.text(),
        #            'data': []
        #        })
        #        json.dump(data, file, ensure_ascii=False)
        #    else:
        #        gestures = data[self.label_2.text()]
        #        gestures['Жесты']['data'].append(arr)
        #        json.dump(data, file, ensure_ascii=False)
        if isFileOpened:
                a = self.textEdit.toPlainText()
                data[self.textEdit.toPlainText()] = {}
                gestures = data[self.textEdit.toPlainText()]
                gestures['Жесты'] = []
                gestures['Жесты'].append({
                    'name': 'жест',
                    'index': self.textEdit_2.toPlainText(),
                    'data': arr
                })
                json.dump(data, file, ensure_ascii=False)

def operateData(self, file):
        global isFileOpened
        if self.pushButton_2.text()=='Начать запись':
          #  global isFileOpened
            isFileOpened = True
            file = open('data.json', 'w', encoding='utf-8')
            self.pushButton_2.setText('Остановить запись')
        else:
          #  global isFileOpened
            isFileOpened = False
            file.close()
            self.pushButton_2.setText('Начать запись')

class Canvas(FigureCanvas):
    def __init__(self, parent):
        fig, self.ax = plt.subplots(figsize=(4, 2), dpi=190)
        super().__init__(fig)
        self.setParent(parent)

        """ 
        
        Вывод 
        графика

        """

        Z1 = np.zeros((9, 31))   # инициализация матрицы, на 1 меньше по осям по сравнению с x и y

        self.Z = Z1
        x = np.arange(0, 32, 1)  # len = 32, число каналов
        y = np.arange(0, 10, 1)  # len = 11, число за раз выводимых показаний

        self.cur_step = 0

        self.ax.pcolormesh(x, y, self.Z)


class Ui_MainWindow(object):
    serialInst = serial.Serial()
    serialInst.baudrate = 115200

    def changeButtText(self, file):
        if self.pushButton.text() == "Подключиться":
            self.pushButton.setText("Отключиться")

            self.serialInst.port = self.comboBox.currentText()
            self.serialInst.open()
            print("Port has been initialized")

            # создание таймера
            self.timer = QtCore.QTimer()

            # добавление действия по истечению времени
            self.timer.timeout.connect(lambda: handle_available_data(self, file))

            # время (обновления) таймера
            self.timer.start(50)


        elif self.pushButton.text() == "Отключиться":
            self.pushButton.setText("Подключиться")
            self.serialInst.close()



    def setupUi(self, MainWindow):
        file = open('data.json', 'w', encoding='utf-8')

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(10, 50, 171, 41))
        self.comboBox.setObjectName("comboBox")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 191, 31))

        font = QtGui.QFont()
        font.setPointSize(13)

        self.label.setFont(font)
        self.label.setObjectName("label")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 110, 171, 51))

        font = QtGui.QFont()
        font.setPointSize(13)

        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(lambda: self.changeButtText(file))

        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(20, 170, 751, 391))
        self.widget.setAutoFillBackground(False)
        self.widget.setStyleSheet("border-color: rgb(8, 8, 8);")
        self.widget.setObjectName("widget")

        MainWindow.setCentralWidget(self.centralwidget)

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(220, 110, 171, 51))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(lambda: operateData(self, file))
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(430, 10, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(680, 10, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(420, 50, 141, 31))
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(630, 50, 141, 31))
        self.textEdit_2.setObjectName("textEdit_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        MainWindow.setStatusBar(self.statusbar)

        """

        Создание 
        графика

        """

        global chart
        chart = Canvas(self.widget)

        """
        
        Получение и вывод доступных ком-портов
        
        """
        port_info = []
        ports = serial.tools.list_ports.comports()
        for port, desc, hwid in sorted(ports):
            print("{}: {} [{}]".format(port, desc, hwid))
            port_info.append(port)

        self.comboBox.addItems(port_info)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Данные с датчиков браслета"))
        self.label.setText(_translate("MainWindow", "Доступные com-порты"))
        self.pushButton.setText(_translate("MainWindow", "Подключиться"))
        self.pushButton_2.setText(_translate("MainWindow", "Начать запись"))
        self.label_2.setText(_translate("MainWindow", "Пользователь"))
        self.label_3.setText(_translate("MainWindow", "Жест"))