import os
import serial.tools.list_ports
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from handlers import handle_ready_read, handle_error, convert_input_data, num_channels, chart_height, chart_width, process_data
from mainwindow_ui import Ui_MainWindow
import json
from canvas import Canvas, AnimatedCanvas, AverageCanvas

isFileOpened = False
chart = None

SETTINGS_FILE = "settings.json"


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, min_value=-32768, max_value=32767, record_interval=2000):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.showMaximized()

        self.serialInst = serial.Serial()
        self.serialInst.baudrate = 115200
        self.is_recording = False

        self.load_settings()

        self.chart = Canvas(self, chart_height=chart_height,
                            chart_width=chart_width, min_value=self.min_value, max_value=self.max_value)
        self.gridLayout_2.addWidget(self.chart, 3, 3, 2, 4)

        self.connect_button.clicked.connect(self.toggle_connection)
        self.startrecording_button.clicked.connect(self.toggle_recording)
        self.min_slider.valueChanged.connect(self.update_min_value)
        self.max_slider.valueChanged.connect(self.update_max_value)
        self.adduser_button.clicked.connect(self.add_user)
        self.addgestre_button.clicked.connect(self.add_gesture)
        self.delete_button.clicked.connect(self.delete_selected)
        self.duration_combobox.textChanged.connect(self.update_record_interval)
        self.graph1_combobox.currentIndexChanged.connect(
            self.update_graph1_channel)
        self.graph2_combobox.currentIndexChanged.connect(
            self.update_graph2_channel)

        self.comport_combobox.addItems(
            [port.device for port in serial.tools.list_ports.comports()])
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(lambda: self.handle_available_data())

        self.connected = False
        self.update_min_value()
        self.update_max_value()
        self.data_buffer = []

        self.model = QtGui.QStandardItemModel()
        self.data_treeview.setModel(self.model)
        self.load_existing_data()
        self.load_combobox_data()

        self.avg_canvases = [AverageCanvas(
            self, channels=range(i * 16, (i + 1) * 16)) for i in range(6)]
        for i, avg_canvas in enumerate(self.avg_canvases):
            getattr(self, f'avg{i + 1}').setLayout(QtWidgets.QVBoxLayout())
            getattr(self, f'avg{i + 1}').layout().addWidget(avg_canvas)

        self.graph1_canvas = AnimatedCanvas(self, channel=0)
        self.graph1.setLayout(QtWidgets.QVBoxLayout())
        self.graph1.layout().addWidget(self.graph1_canvas)

        self.graph2_canvas = AnimatedCanvas(self, channel=1)
        self.graph2.setLayout(QtWidgets.QVBoxLayout())
        self.graph2.layout().addWidget(self.graph2_canvas)

        self.graph1_combobox.addItems([str(i) for i in range(1, 97)])
        self.graph2_combobox.addItems([str(i) for i in range(1, 97)])
        self.graph1_combobox.setCurrentIndex(0)
        self.graph2_combobox.setCurrentIndex(1)

    def update_graph1_channel(self):
        channel = int(self.graph1_combobox.currentText()) - 1
        self.graph1_canvas.update_channel(channel)

    def update_graph2_channel(self):
        channel = int(self.graph2_combobox.currentText()) - 1
        self.graph2_canvas.update_channel(channel)

    def handle_available_data(self):
        if self.serialInst.isOpen():
            handle_ready_read(self)
            if self.data_buffer:  # Проверяем, что буфер не пуст
                new_data = self.data_buffer[-1]  # Последние полученные данные
                for avg_canvas in self.avg_canvases:
                    avg_canvas.update_plot(new_data)
                self.graph1_canvas.update_plot(new_data)
                self.graph2_canvas.update_plot(new_data)

    def toggle_connection(self):
        if not self.connected:
            self.data_buffer = []  # Инициализируем буфер данных при подключении
            self.connect_serial()
        else:
            self.disconnect_serial()

    def connect_serial(self):
        try:
            self.serialInst.port = self.comport_combobox.currentText()
            self.serialInst.open()
            self.update_state("Порт был инициализирован")
            self.timer.start(1)
            self.connect_button.setText("Отключиться")
            self.connected = True
        except Exception as e:
            self.update_state(f"Ошибка при подключении к порту: {str(e)}")

    def disconnect_serial(self):
        self.serialInst.close()
        self.timer.stop()
        self.update_state("Порт был закрыт")
        self.connect_button.setText("Подключиться")
        self.connected = False

    def toggle_recording(self):
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        self.is_recording = True
        self.startrecording_button.setText("Остановить запись")
        QtCore.QTimer.singleShot(
            self.record_interval, self.stop_recording)

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            self.save_recorded_data()
            self.startrecording_button.setText("Начать запись")

    def save_recorded_data(self):
        user = self.user_combobox.currentText()
        gesture = self.gesture_commbobox.currentText()

        if not user or not gesture:
            self.update_state("Пользователь или жест не выбран")
            return

        user_folder = os.path.join("data", user)
        os.makedirs(user_folder, exist_ok=True)
        gesture_file = os.path.join(user_folder, f"{gesture}.json")

        try:
            with open(gesture_file, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"name": gesture, "index": 1, "data": []}

        processed_data = [process_data(row) for row in self.data_buffer]
        transposed_data = list(map(list, zip(*processed_data)))
        data["data"].append(transposed_data)

        with open(gesture_file, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        self.data_buffer = []  # Очищаем буфер данных после сохранения
        self.load_existing_data()  # Обновление QTreeView
        self.load_combobox_data()  # Обновление combobox

    def add_user(self):
        user_name = self.user_lineedit.text().strip()
        if user_name and self.user_combobox.findText(user_name) == -1:
            self.user_combobox.addItem(user_name)
            os.makedirs(os.path.join("data", user_name), exist_ok=True)
            self.user_lineedit.clear()
            self.load_existing_data()  # Обновление QTreeView
            self.update_state(f"Пользователь {user_name} добавлен")

    def add_gesture(self):
        gesture_name = self.gesture_lineedit.text().strip()
        if gesture_name:
            try:
                with open("gestures.json", "r", encoding="utf-8") as file:
                    gestures = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                gestures = []

            if gesture_name not in [g["name"] for g in gestures]:
                gesture_index = len(gestures) + 1
                gestures.append({"name": gesture_name, "index": gesture_index})

                with open("gestures.json", "w", encoding="utf-8") as file:
                    json.dump(gestures, file, ensure_ascii=False, indent=4)

                if self.gesture_commbobox.findText(gesture_name) == -1:
                    self.gesture_commbobox.addItem(gesture_name)
                    self.gesture_lineedit.clear()
                    self.update_state(f"Жест {gesture_name} добавлен")
                    self.load_combobox_data()  # Обновление combobox

    def delete_selected(self):
        index = self.data_treeview.currentIndex()
        item = self.model.itemFromIndex(index)
        if not item:
            self.update_state("Не выбран элемент для удаления")
            return

        parent = item.parent()
        if not parent:  # Удаляем пользователя
            user_folder = os.path.join("data", item.text())
            if os.path.isdir(user_folder):
                os.rmdir(user_folder)
                self.update_state(f"Папка пользователя {item.text()} удалена")
        else:
            if parent.text() == "Жесты":  # Удаляем жест
                user_item = parent.parent()
                user_folder = os.path.join("data", user_item.text())
                gesture_file = os.path.join(user_folder, f"{item.text()}.json")
                if os.path.isfile(gesture_file):
                    os.remove(gesture_file)
                    self.update_state(f"Файл жеста {item.text()} удален")
            else:  # Удаляем запись жеста
                user_item = parent.parent().parent()
                user_folder = os.path.join("data", user_item.text())
                gesture_file = os.path.join(
                    user_folder, f"{parent.text()}.json")
                if os.path.isfile(gesture_file):
                    with open(gesture_file, "r", encoding="utf-8") as file:
                        gesture_data = json.load(file)
                    gesture_data["data"].pop(item.row())
                    with open(gesture_file, "w", encoding="utf-8") as file:
                        json.dump(gesture_data, file,
                                  ensure_ascii=False, indent=4)
                    self.update_state(f"Запись {item.text()} удалена")

        self.load_existing_data()
        self.load_combobox_data()  # Обновление combobox

    def update_min_value(self):
        min_value = self.min_slider.value()
        self.chart.set_min_value(min_value)
        self.update_state(f"Минимальное значение обновлено до {min_value}")

    def update_max_value(self):
        max_value = self.max_slider.value()
        self.chart.set_max_value(max_value)
        self.update_state(f"Максимальное значение обновлено до {max_value}")

    def update_record_interval(self):
        try:
            self.record_interval = int(self.duration_combobox.text())
            self.update_state(
                f"Длительность записи обновлена до {self.record_interval} мс")
            self.save_settings()
        except ValueError:
            self.update_state("Некорректное значение длительности записи")

    def save_expanded_items(self):
        expanded_items = []
        root = self.model.invisibleRootItem()
        for i in range(root.rowCount()):
            item = root.child(i)
            if self.data_treeview.isExpanded(self.model.indexFromItem(item)):
                expanded_items.append(item.text())
            for j in range(item.rowCount()):
                child_item = item.child(j)
                if self.data_treeview.isExpanded(self.model.indexFromItem(child_item)):
                    expanded_items.append(child_item.text())
                for k in range(child_item.rowCount()):
                    grandchild_item = child_item.child(k)
                    if self.data_treeview.isExpanded(self.model.indexFromItem(grandchild_item)):
                        expanded_items.append(grandchild_item.text())
        return expanded_items

    def restore_expanded_items(self, expanded_items):
        root = self.model.invisibleRootItem()
        for i in range(root.rowCount()):
            item = root.child(i)
            if item.text() in expanded_items:
                self.data_treeview.setExpanded(
                    self.model.indexFromItem(item), True)
            for j in range(item.rowCount()):
                child_item = item.child(j)
                if child_item.text() in expanded_items:
                    self.data_treeview.setExpanded(
                        self.model.indexFromItem(child_item), True)
                for k in range(child_item.rowCount()):
                    grandchild_item = child_item.child(k)
                    if grandchild_item.text() in expanded_items:
                        self.data_treeview.setExpanded(
                            self.model.indexFromItem(grandchild_item), True)

    def load_existing_data(self):
        expanded_items = self.save_expanded_items()

        self.model.clear()
        root = self.model.invisibleRootItem()
        data_folder = "data"

        if os.path.exists(data_folder):
            for user_folder in os.listdir(data_folder):
                user_path = os.path.join(data_folder, user_folder)
                if os.path.isdir(user_path):
                    user_item = QtGui.QStandardItem(user_folder)
                    root.appendRow(user_item)
                    gesture_folder_item = QtGui.QStandardItem("Жесты")
                    user_item.appendRow(gesture_folder_item)
                    for gesture_file in os.listdir(user_path):
                        gesture_path = os.path.join(user_path, gesture_file)
                        if os.path.isfile(gesture_path) and gesture_file.endswith(".json"):
                            with open(gesture_path, "r", encoding="utf-8") as file:
                                gesture_data = json.load(file)
                            gesture_name = gesture_data.get(
                                "name", os.path.splitext(gesture_file)[0])
                            gesture_item = QtGui.QStandardItem(gesture_name)
                            gesture_folder_item.appendRow(gesture_item)
                            for idx, record in enumerate(gesture_data.get("data", [])):
                                record_item = QtGui.QStandardItem(
                                    f"Запись {idx + 1}")
                                gesture_item.appendRow(record_item)

        self.restore_expanded_items(expanded_items)

    def load_combobox_data(self):
        self.user_combobox.clear()
        self.gesture_commbobox.clear()

        data_folder = "data"
        if os.path.exists(data_folder):
            for user_folder in os.listdir(data_folder):
                user_path = os.path.join(data_folder, user_folder)
                if os.path.isdir(user_path):
                    self.user_combobox.addItem(user_folder)

        try:
            with open("gestures.json", "r", encoding="utf-8") as file:
                gestures = json.load(file)
                for gesture in gestures:
                    self.gesture_commbobox.addItem(gesture["name"])
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def load_settings(self):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
                settings = json.load(file)
                self.min_value = settings.get("min_value", -32768)
                self.max_value = settings.get("max_value", 32767)
                self.record_interval = settings.get("record_interval", 2000)
                self.min_slider.setValue(int((self.min_value / 3276.8) + 15))
                self.max_slider.setValue(int((self.max_value / 3276.8) + 15))
                self.duration_combobox.setText(str(self.record_interval))
        except (FileNotFoundError, json.JSONDecodeError):
            self.min_value = -32768
            self.max_value = 32767
            self.record_interval = 2000

    def save_settings(self):
        settings = {
            "min_value": self.min_value,
            "max_value": self.max_value,
            "record_interval": self.record_interval
        }
        with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
            json.dump(settings, file, ensure_ascii=False, indent=4)

    def update_plot(self, value):
        self.chart.update_plot(value)

    def record_data(self, data):
        self.data_buffer.append(data)

    def update_state(self, message):
        self.state_label.setText(message)
        print(message)
