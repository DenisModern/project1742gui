from interface import *


def update_plot(self, value):
    self.y = self.y[1:] + [value]
    self.x = self.x[1:]
    self.x.append(self.x[-1] + 1)
    self.data_line.setData(self.x, self.y)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
