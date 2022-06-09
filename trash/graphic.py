import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QWidget, QApplication, QSizePolicy
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.grid = QtWidgets.QHBoxLayout()
        self.setLayout(self.grid)
        self.figure = plt.figure()
        self.canv = FigureCanvas(self.figure)
        self.grid.addWidget(self.canv)
        self.graph_draw()

    def graph_draw(self):
        x = [1,2,3,4]
        y = [2,4,1,2]
        plt.plot(x,y)
        self.canv.draw()


app = QApplication(sys.argv)
if __name__ == '__main__':
    gui = Window()
    gui.show()
    sys.exit(app.exec_())
