import sys
import serial.tools.list_ports
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets, QtSerialPort

def handle_ready_read(self):
    while self.serial_port.canReadLine():
        codec = QtCore.QTextCodec.codecForName("UTF-8")
        line = codec.toUnicode(self.serial_port.readLine()).strip().strip('\x00')
        try:
            print(line)
            value = float(line)
        except ValueError as e:
            print("error", e)
        else:
            self.update_plot(value)

def handle_error(self, error):
    if error == QtSerialPort.QSerialPort.NoError:
        return
    print(error, self.serial_port.errorString())

"""
Функция считывает данные из серийного порта, 
если он открыт, и декодирует их
"""
def handle_available_data(self):
    if self.serialInst.isOpen():
        packet = self.serialInst.readline()
        data =packet.decode('ascii', errors='ignore').rstrip('\n')
        data = data.strip('\r')
        print(data)
        convert_input_data(chart, data)

def update_plot(self, value):
    self.y = self.y[1:] + [value]
    self.x = self.x[1:]
    self.x.append(self.x[-1] + 1)
    self.data_line.setData(self.x, self.y)

"""
Функция преобразует полученную строку данных
"""
def convert_input_data(self, str1):
    Z1 = []
    Z1 = str1.split()
    display_input_data(self, Z1, self.cur_step)

"""
Функция перерисовывает график в реальном времени
"""
def display_input_data(self, Z1, cur_step):
    for i in range(len(Z1)-1):
        try:
            self.Z[cur_step % 9][i] = Z1[i]
        except ValueError:
            continue
    self.draw()
    self.flush_events()
    x = np.arange(0, 32, 1)  # len = 10
    y = np.arange(0, 10, 1)  # len = 32
    self.ax.pcolormesh(x, y, self.Z)
    self.cur_step+=1

class Canvas(FigureCanvas):
    def __init__(self, parent):
        fig, self.ax = plt.subplots(figsize=(4, 2), dpi=190)
        super().__init__(fig)
        self.setParent(parent)

        """ 
        
        Вывод 
        графика
        
        """

        Z1 = np.zeros((9, 31))

        self.Z = Z1
        x = np.arange(0, 32, 1)  # len = 32
        y = np.arange(0, 10, 1)  # len = 11

        self.cur_step = 0

        self.ax.pcolormesh(x, y, self.Z)

class Ui_MainWindow(object):
    serialInst = serial.Serial()
    serialInst.baudrate = 115200
    def changeButtText(self):
        if self.pushButton.text() == "Подключиться":
            self.pushButton.setText("Отключиться")

            self.serialInst.port = self.comboBox.currentText()
            self.serialInst.open()
            print("Port has been initialized")

            # создание таймера
            self.timer = QtCore.QTimer()

            # добавление действия по истечению времени
            self.timer.timeout.connect(lambda: handle_available_data(self))

            # время (обновления) таймера
            self.timer.start(50)


        elif self.pushButton.text() == "Отключиться":
            self.pushButton.setText("Подключиться")
            self.serialInst.close()

    def setupUi(self, MainWindow):
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
        self.pushButton.clicked.connect(self.changeButtText)

        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(20, 170, 751, 391))
        self.widget.setAutoFillBackground(False)
        self.widget.setStyleSheet("border-color: rgb(8, 8, 8);")
        self.widget.setObjectName("widget")

        MainWindow.setCentralWidget(self.centralwidget)

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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
