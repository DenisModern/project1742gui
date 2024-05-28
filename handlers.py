from PyQt5 import QtCore, QtSerialPort
import numpy as np


def handle_ready_read(self):
    while self.serial_port.canReadLine():
        codec = QtCore.QTextCodec.codecForName("UTF-8")
        line = codec.toUnicode(
            self.serial_port.readLine()).strip().strip('\x00')
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
Функция преобразует полученную строку данных
"""


def convert_input_data(self, str1):
    Z1 = []
    Z1 = str1.split(', ')
    display_input_data(self, Z1, self.cur_step)
    return Z1


"""
Функция перерисовывает график в реальном времени
"""


def display_input_data(self, Z1, cur_step):
    l = 0
    if len(Z1) > 95:
        l = 95
    else:
        l = len(Z1)
    for i in range(l):
        try:
            self.Z[cur_step % 9][i] = Z1[i]
        except ValueError:
            continue
    self.draw()
    self.flush_events()
    x = np.arange(0, 96, 1)  # len = 96
    y = np.arange(0, 10, 1)  # len = 10
    self.ax.pcolormesh(x, y, self.Z)
    self.cur_step += 1
