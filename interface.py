import serial.tools.list_ports
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from handlers import handle_ready_read, handle_error, convert_input_data, num_channels, chart_height, chart_width
from mainwindow_ui import Ui_MainWindow
import json
# Предполагаем, что Canvas класс теперь находится в отдельном файле canvas.py
from canvas import Canvas

isFileOpened = False
chart = None


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, sensitivity=1.0):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.serialInst = serial.Serial()
        self.serialInst.baudrate = 115200

        # Найти виджет для графика и добавить в него Canvas
        self.chart = Canvas(self, chart_height=chart_height,
                            chart_width=chart_width, sensitivity=sensitivity)
        self.gridLayout_2.addWidget(self.chart, 2, 6, 2, 2)

        self.connect_button.clicked.connect(self.toggle_connection)
        self.startrecording_button.clicked.connect(self.operate_data)
        self.sensetivity_slider.valueChanged.connect(self.update_sensitivity)

        self.comport_combobox.addItems(
            [port.device for port in serial.tools.list_ports.comports()])
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(lambda: self.handle_available_data())

        self.connected = False
        self.update_sensitivity()

    def toggle_connection(self):
        if not self.connected:
            self.connect_serial()
        else:
            self.disconnect_serial()

    def connect_serial(self):
        self.serialInst.port = self.comport_combobox.currentText()
        self.serialInst.open()
        print("Port has been initialized")
        self.timer.start(50)
        self.connect_button.setText("Отключиться")
        self.connected = True

    def disconnect_serial(self):
        self.serialInst.close()
        self.timer.stop()
        print("Port has been closed")
        self.connect_button.setText("Подключиться")
        self.connected = False

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
            handle_ready_read(self)

    def update_sensitivity(self):
        sensitivity_value = self.sensetivity_slider.value() / 10  # Диапазон от 0.1 до 3.0
        self.chart.set_sensitivity(sensitivity_value)
        print(f"Updated sensitivity to {sensitivity_value}")

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
