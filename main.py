from interface import MainWindow
from PyQt5 import QtWidgets
import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    sensitivity = 1.0  # Значение по умолчанию
    if len(sys.argv) > 1:
        try:
            sensitivity = float(sys.argv[1])
        except ValueError:
            print("Invalid sensitivity value, using default (1.0)")

    mainWindow = MainWindow(sensitivity=sensitivity)
    mainWindow.show()
    sys.exit(app.exec_())
