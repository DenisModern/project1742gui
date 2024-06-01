# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\project1742gui\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1316, 727)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("QWidget#centralwidget {\n"
"    background-color: #2E2E2E;  /* Темный фон */\n"
"    color: #E0E0E0;  /* Светлый текст */\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #E0E0E0;  /* Светлый текст */\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background-color: #3A3A3A;  /* Темный фон кнопок */\n"
"    color: #E0E0E0;  /* Светлый текст */\n"
"    border: 1px solid #1E90FF;  /* Ледяной синий бордюр */\n"
"    padding: 5px 10px;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #1E90FF;  /* Ледяной синий при наведении */\n"
"}\n"
"\n"
"QLineEdit, QComboBox, QTreeView, QSlider::groove:horizontal {\n"
"    background-color: #3A3A3A;  /* Темный фон для ввода текста, выпадающих списков и слайдеров */\n"
"    color: #E0E0E0;  /* Светлый текст */\n"
"    border: 1px solid #1E90FF;  /* Ледяной синий бордюр */\n"
"    padding: 5px;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 20px;\n"
"    border-left-width: 1px;\n"
"    border-left-color: #1E90FF;\n"
"    border-left-style: solid;\n"
"    border-top-right-radius: 5px;\n"
"    border-bottom-right-radius: 5px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(down_arrow.png);  /* Путь к иконке стрелки вниз */\n"
"    width: 12px;\n"
"    height: 12px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    background: #1E90FF;  /* Ледяной синий бегунок */\n"
"    border: 1px solid #3A3A3A;\n"
"    width: 10px;\n"
"    margin: -5px 0; /* Уменьшение области клика */\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QSlider::groove:horizontal {\n"
"    height: 10px;\n"
"    background: #3A3A3A;\n"
"    border: 1px solid #1E90FF;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"#numrecordings_label {\n"
"    font: 18pt \"Segoe UI\";\n"
"}\n"
"")
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.avg1 = QtWidgets.QWidget(self.centralwidget)
        self.avg1.setObjectName("avg1")
        self.verticalLayout_2.addWidget(self.avg1)
        self.avg2 = QtWidgets.QWidget(self.centralwidget)
        self.avg2.setObjectName("avg2")
        self.verticalLayout_2.addWidget(self.avg2)
        self.avg3 = QtWidgets.QWidget(self.centralwidget)
        self.avg3.setMinimumSize(QtCore.QSize(100, 0))
        self.avg3.setObjectName("avg3")
        self.verticalLayout_2.addWidget(self.avg3)
        self.avg4 = QtWidgets.QWidget(self.centralwidget)
        self.avg4.setObjectName("avg4")
        self.verticalLayout_2.addWidget(self.avg4)
        self.avg5 = QtWidgets.QWidget(self.centralwidget)
        self.avg5.setObjectName("avg5")
        self.verticalLayout_2.addWidget(self.avg5)
        self.avg6 = QtWidgets.QWidget(self.centralwidget)
        self.avg6.setObjectName("avg6")
        self.verticalLayout_2.addWidget(self.avg6)
        self.gridLayout_3.addLayout(self.verticalLayout_2, 0, 3, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.data_treeview = QtWidgets.QTreeView(self.centralwidget)
        self.data_treeview.setObjectName("data_treeview")
        self.gridLayout_2.addWidget(self.data_treeview, 3, 0, 2, 3)
        self.gesture1_label = QtWidgets.QLabel(self.centralwidget)
        self.gesture1_label.setObjectName("gesture1_label")
        self.gridLayout_2.addWidget(self.gesture1_label, 2, 0, 1, 1)
        self.user_label = QtWidgets.QLabel(self.centralwidget)
        self.user_label.setObjectName("user_label")
        self.gridLayout_2.addWidget(self.user_label, 1, 0, 1, 1)
        self.user_lineedit = QtWidgets.QLineEdit(self.centralwidget)
        self.user_lineedit.setObjectName("user_lineedit")
        self.gridLayout_2.addWidget(self.user_lineedit, 1, 1, 1, 1)
        self.activitymap = QtWidgets.QWidget(self.centralwidget)
        self.activitymap.setObjectName("activitymap")
        self.gridLayout_2.addWidget(self.activitymap, 3, 3, 2, 4)
        self.state_label = QtWidgets.QLabel(self.centralwidget)
        self.state_label.setObjectName("state_label")
        self.gridLayout_2.addWidget(self.state_label, 7, 0, 1, 3)
        self.duration_label = QtWidgets.QLabel(self.centralwidget)
        self.duration_label.setObjectName("duration_label")
        self.gridLayout_2.addWidget(self.duration_label, 2, 3, 1, 1)
        self.graph2_combobox = QtWidgets.QComboBox(self.centralwidget)
        self.graph2_combobox.setObjectName("graph2_combobox")
        self.gridLayout_2.addWidget(self.graph2_combobox, 7, 6, 1, 1)
        self.delete_button = QtWidgets.QPushButton(self.centralwidget)
        self.delete_button.setObjectName("delete_button")
        self.gridLayout_2.addWidget(self.delete_button, 5, 0, 1, 1)
        self.startrecording_button = QtWidgets.QPushButton(self.centralwidget)
        self.startrecording_button.setObjectName("startrecording_button")
        self.gridLayout_2.addWidget(self.startrecording_button, 0, 3, 1, 4)
        self.connect_label = QtWidgets.QLabel(self.centralwidget)
        self.connect_label.setObjectName("connect_label")
        self.gridLayout_2.addWidget(self.connect_label, 0, 0, 1, 1)
        self.gesture2_label = QtWidgets.QLabel(self.centralwidget)
        self.gesture2_label.setObjectName("gesture2_label")
        self.gridLayout_2.addWidget(self.gesture2_label, 1, 5, 1, 1)
        self.graph1_combobox = QtWidgets.QComboBox(self.centralwidget)
        self.graph1_combobox.setObjectName("graph1_combobox")
        self.gridLayout_2.addWidget(self.graph1_combobox, 7, 4, 1, 1)
        self.adduser_button = QtWidgets.QPushButton(self.centralwidget)
        self.adduser_button.setObjectName("adduser_button")
        self.gridLayout_2.addWidget(self.adduser_button, 1, 2, 1, 1)
        self.gesture_commbobox = QtWidgets.QComboBox(self.centralwidget)
        self.gesture_commbobox.setObjectName("gesture_commbobox")
        self.gridLayout_2.addWidget(self.gesture_commbobox, 1, 6, 1, 1)
        self.graph1 = QtWidgets.QWidget(self.centralwidget)
        self.graph1.setObjectName("graph1")
        self.gridLayout_2.addWidget(self.graph1, 6, 3, 1, 2)
        self.min_slider = QtWidgets.QSlider(self.centralwidget)
        self.min_slider.setMinimum(-32768)
        self.min_slider.setMaximum(32767)
        self.min_slider.setPageStep(1)
        self.min_slider.setProperty("value", 0)
        self.min_slider.setOrientation(QtCore.Qt.Horizontal)
        self.min_slider.setObjectName("min_slider")
        self.gridLayout_2.addWidget(self.min_slider, 5, 4, 1, 1)
        self.max_label = QtWidgets.QLabel(self.centralwidget)
        self.max_label.setObjectName("max_label")
        self.gridLayout_2.addWidget(self.max_label, 5, 5, 1, 1)
        self.user2_label = QtWidgets.QLabel(self.centralwidget)
        self.user2_label.setObjectName("user2_label")
        self.gridLayout_2.addWidget(self.user2_label, 1, 3, 1, 1)
        self.addgestre_button = QtWidgets.QPushButton(self.centralwidget)
        self.addgestre_button.setObjectName("addgestre_button")
        self.gridLayout_2.addWidget(self.addgestre_button, 2, 2, 1, 1)
        self.graph2 = QtWidgets.QWidget(self.centralwidget)
        self.graph2.setObjectName("graph2")
        self.gridLayout_2.addWidget(self.graph2, 6, 5, 1, 2)
        self.graph2_label = QtWidgets.QLabel(self.centralwidget)
        self.graph2_label.setObjectName("graph2_label")
        self.gridLayout_2.addWidget(self.graph2_label, 7, 5, 1, 1)
        self.connect_button = QtWidgets.QPushButton(self.centralwidget)
        self.connect_button.setObjectName("connect_button")
        self.gridLayout_2.addWidget(self.connect_button, 0, 2, 1, 1)
        self.graph1_label = QtWidgets.QLabel(self.centralwidget)
        self.graph1_label.setObjectName("graph1_label")
        self.gridLayout_2.addWidget(self.graph1_label, 7, 3, 1, 1)
        self.gesture_lineedit = QtWidgets.QLineEdit(self.centralwidget)
        self.gesture_lineedit.setObjectName("gesture_lineedit")
        self.gridLayout_2.addWidget(self.gesture_lineedit, 2, 1, 1, 1)
        self.user_combobox = QtWidgets.QComboBox(self.centralwidget)
        self.user_combobox.setObjectName("user_combobox")
        self.gridLayout_2.addWidget(self.user_combobox, 1, 4, 1, 1)
        self.min_label = QtWidgets.QLabel(self.centralwidget)
        self.min_label.setObjectName("min_label")
        self.gridLayout_2.addWidget(self.min_label, 5, 3, 1, 1)
        self.ms_label = QtWidgets.QLabel(self.centralwidget)
        self.ms_label.setObjectName("ms_label")
        self.gridLayout_2.addWidget(self.ms_label, 2, 5, 1, 1)
        self.max_slider = QtWidgets.QSlider(self.centralwidget)
        self.max_slider.setMinimum(-32768)
        self.max_slider.setMaximum(32767)
        self.max_slider.setPageStep(1)
        self.max_slider.setProperty("value", 0)
        self.max_slider.setOrientation(QtCore.Qt.Horizontal)
        self.max_slider.setObjectName("max_slider")
        self.gridLayout_2.addWidget(self.max_slider, 5, 6, 1, 1)
        self.duration_combobox = QtWidgets.QLineEdit(self.centralwidget)
        self.duration_combobox.setObjectName("duration_combobox")
        self.gridLayout_2.addWidget(self.duration_combobox, 2, 4, 1, 1)
        self.comport_combobox = QtWidgets.QComboBox(self.centralwidget)
        self.comport_combobox.setObjectName("comport_combobox")
        self.gridLayout_2.addWidget(self.comport_combobox, 0, 1, 1, 1)
        self.com_textedit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.com_textedit.setObjectName("com_textedit")
        self.gridLayout_2.addWidget(self.com_textedit, 6, 0, 1, 3)
        self.rec_label = QtWidgets.QLabel(self.centralwidget)
        self.rec_label.setObjectName("rec_label")
        self.gridLayout_2.addWidget(self.rec_label, 2, 6, 1, 1)
        self.numrecordingstext_label = QtWidgets.QLabel(self.centralwidget)
        self.numrecordingstext_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.numrecordingstext_label.setObjectName("numrecordingstext_label")
        self.gridLayout_2.addWidget(self.numrecordingstext_label, 5, 1, 1, 1)
        self.numrecordings_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(False)
        self.numrecordings_label.setFont(font)
        self.numrecordings_label.setAlignment(QtCore.Qt.AlignCenter)
        self.numrecordings_label.setObjectName("numrecordings_label")
        self.gridLayout_2.addWidget(self.numrecordings_label, 5, 2, 1, 1)
        self.gridLayout_2.setColumnStretch(4, 1)
        self.gridLayout_2.setColumnStretch(6, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 1, 1, 1)
        self.gridLayout_3.setColumnStretch(3, 2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.gesture1_label.setText(_translate("MainWindow", "Жест"))
        self.user_label.setText(_translate("MainWindow", "Испытуемый"))
        self.state_label.setText(_translate("MainWindow", "Состояние"))
        self.duration_label.setText(_translate("MainWindow", "Длительность жеста"))
        self.delete_button.setText(_translate("MainWindow", "Удалить"))
        self.startrecording_button.setText(_translate("MainWindow", "Начать запись"))
        self.connect_label.setText(_translate("MainWindow", "Порт"))
        self.gesture2_label.setText(_translate("MainWindow", "Жест"))
        self.adduser_button.setText(_translate("MainWindow", "Добавить"))
        self.max_label.setText(_translate("MainWindow", "Максимальное"))
        self.user2_label.setText(_translate("MainWindow", "Пользователь"))
        self.addgestre_button.setText(_translate("MainWindow", "Добавить"))
        self.graph2_label.setText(_translate("MainWindow", "График 2"))
        self.connect_button.setText(_translate("MainWindow", "Подключиться"))
        self.graph1_label.setText(_translate("MainWindow", "График 1"))
        self.min_label.setText(_translate("MainWindow", "Минимальное"))
        self.ms_label.setText(_translate("MainWindow", "миллисекунд"))
        self.rec_label.setText(_translate("MainWindow", "Запись не идет"))
        self.numrecordingstext_label.setText(_translate("MainWindow", "Записей жеста"))
        self.numrecordings_label.setText(_translate("MainWindow", "0"))
