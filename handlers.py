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


def convert_input_data(self, str1):
    Z1 = str1.split(', ')
    display_input_data(self, Z1, self.cur_step)
    return Z1


def display_input_data(self, Z1, cur_step):
    l = len(Z1) if len(Z1) <= 95 else 95
    for i in range(l):
        try:
            self.Z[cur_step % 9][i] = Z1[i]
        except ValueError:
            continue
    self.draw()
    self.flush_events()
    self.cur_step += 1
