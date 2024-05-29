from PyQt5 import QtCore, QtSerialPort
import numpy as np

num_channels = 32  # Количество каналов, может быть изменено
chart_height = 8  # Высота карты активности, может быть изменена
chart_width = num_channels // chart_height  # Ширина карты активности

data_buffer = b''  # Буфер для частично полученных данных


def handle_ready_read(self):
    global data_buffer
    while self.serialInst.in_waiting > 0:
        data_buffer += self.serialInst.read(self.serialInst.in_waiting)
        # Отладочное сообщение для символьного вида данных
        print(f"Buffer data: {data_buffer}")

        # Разделим буфер на строки
        lines = data_buffer.split(b'\n')

        for line in lines[:-1]:  # Обработаем все полные строки
            data = list(map(int, line.split()))
            if len(data) == num_channels:
                print(f"Received data: {data}")  # Отладочное сообщение
                self.update_plot(data)
            else:
                print(f"Incorrect data length: {len(data)}")

        data_buffer = lines[-1]  # Оставим неполную строку в буфере


def handle_error(self, error):
    if error == QtSerialPort.QSerialPort.NoError:
        return
    print(error, self.serialInst.errorString())


def convert_input_data(self, data):
    display_input_data(self, data, self.cur_step)
    return data


def display_input_data(self, data, cur_step):
    l = len(data) if len(data) <= num_channels else num_channels
    for i in range(l):
        try:
            self.Z[cur_step % chart_height][i] = data[i]
        except ValueError:
            continue
    self.draw()
    self.flush_events()
    self.cur_step += 1
