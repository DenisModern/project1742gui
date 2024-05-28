import sys
import serial.tools.list_ports
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtCore, QtGui, QtWidgets
from handlers import handle_ready_read, handle_error, convert_input_data
from mainwindow_ui import Ui_MainWindow
import json

isFileOpened = False
chart = None


class Canvas(FigureCanvas):
    def __init__(self, parent=None):
        fig, self.ax = plt.subplots(figsize=(4, 2), dpi=190)
        super().__init__(fig)
        self.setParent(parent)
        self.Z = np.zeros((9, 95))
        x = np.arange(0, 96, 1)
        y = np.arange(0, 10, 1)
        self.cur_step = 0
        self.ax.pcolormesh(x, y, self.Z)

    def update_plot(self, data):
        self.Z[self.cur_step % 9] = data
        self.cur_step += 1
        self.ax.pcolormesh(np.arange(0, 96, 1), np.arange(0, 10, 1), self.Z)
        self.draw()


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.serialInst = serial.Serial()
        self.serialInst.baudrate = 115200

        # Найти виджет для графика и добавить в него Canvas
        self.chart = Canvas(self)
        self.gridLayout_2.addWidget(self.chart, 3, 5, 1, 2)

        self.connect_button.clicked.connect(self.connect_serial)
        self.disconnect_button.clicked.connect(self.disconnect_serial)
        self.startrecording_button.clicked.connect(self.operate_data)

        self.comport_combobox.addItems(
            [port.device for port in serial.tools.list_ports.comports()])
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(lambda: self.handle_available_data())

    def connect_serial(self):
        self.serialInst.port = self.comport_combobox.currentText()
        self.serialInst.open()
        print("Port has been initialized")
        self.timer.start(50)
        self.connect_button.setEnabled(False)
        self.disconnect_button.setEnabled(True)

    def disconnect_serial(self):
        self.serialInst.close()
        self.timer.stop()
        print("Port has been closed")
        self.connect_button.setEnabled(True)
        self.disconnect_button.setEnabled(False)

    def operate_data(self):
        global isFileOpened
        if self.startrecording_button.text() == 'Начать запись':
            isFileOpened = True
            self.file = open('data.json', 'w', encoding='utf-8')
            self.startrecording_button.setText('Остановить запись')
        else:
            isFileOpened = False
            self.file.close()
            self.startrecording_button.setText('Начать запись')

    def handle_available_data(self):
        if self.serialInst.isOpen():
            packet = self.serialInst.readline()
            data = packet.rstrip(b'\n')
            data = list(data)
            data = str(data)
            data = data.replace('[', '').replace(']', '')
            print(data)
            arr = convert_input_data(self.chart, data)
            if isFileOpened:
                json_data = {self.user_lineedit.text(): {"gestures": [
                    {"name": "gesture", "index": self.gesture_lineedit.text(), "data": arr}]}}
                json.dump(json_data, self.file, ensure_ascii=False)

    def load_json_data(self, json_data):
        model = QtGui.QStandardItemModel()
        self.data_treeview.setModel(model)
        self.populate_model(json_data, model.invisibleRootItem())

    def populate_model(self, json_data, parent):
        if isinstance(json_data, dict):
            for key, value in json_data.items():
                key_item = QtGui.QStandardItem(key)
                if isinstance(value, (dict, list)):
                    parent.appendRow(key_item)
                    self.populate_model(value, key_item)
                else:
                    value_item = QtGui.QStandardItem(str(value))
                    parent.appendRow([key_item, value_item])
        elif isinstance(json_data, list):
            for index, value in enumerate(json_data):
                key_item = QtGui.QStandardItem(f"[{index}]")
                if isinstance(value, (dict, list)):
                    parent.appendRow(key_item)
                    self.populate_model(value, key_item)
                else:
                    value_item = QtGui.QStandardItem(str(value))
                    parent.appendRow([key_item, value_item])

    def update_plot(self, value):
        self.chart.update_plot(value)
