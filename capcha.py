import sys
from random import shuffle, randint
from string import ascii_letters

from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsView, QGraphicsScene, QPushButton, QHBoxLayout, \
    QGraphicsTextItem, QLineEdit, QScrollBar


class LoginPage(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = uic.loadUi("untitled.ui", self)
        self.counter = 0
        self.controller = CapthaController()
        self.captha_widget = Captha(self.controller)
        self.captha_line = QLineEdit()
        self.ui.captha_layout.addWidget(self.captha_line)
        self.ui.captha_layout.addWidget(self.captha_widget)
        self.ui.pushButton.clicked.connect(self.auth)

    def auth(self):
        self.counter += 1
        if self.counter == 3:
            self.ui.captha_layout.addWidget(self.captha_line)
            self.ui.captha_layout.addWidget(self.captha_widget)
        elif self.counter < 3:
            self.ui.captha_layout = QHBoxLayout()
        elif self.counter > 8:
            self.ui.captha_layout.deleteLater()


class Captha(QWidget):
    def __init__(self, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.graphics_view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)
        self.graphics_view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphics_view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.update_btn = QPushButton("update")

        self.controller = controller
        self.update_value()

        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.graphics_view, 5)
        self.main_layout.addWidget(self.update_btn, 1)

        self.setLayout(self.main_layout)

        self.update_btn.clicked.connect(self.update_value)

    def update_value(self):
        self.controller.update()
        self.draw_captha()

    def draw_captha(self):
        self.scene.clear()
        for x in range(len(self.controller.get_value())):
            text = self.scene.addText(self.controller.get_value()[x])
            text.moveBy(x * 20, randint(0, 30))


class CapthaController:
    def __init__(self):
        self.update()

    def update(self):
        s = [i for i in ascii_letters]
        shuffle(s)
        digits = [str(i) for i in range(10)]
        shuffle(digits)
        self.generator = s[:4] + digits[:2]
        shuffle(self.generator)

    def get_value(self):
        return self.generator


    def check_captcha(self, s):
        if not s:
            return False
        for i, ch in enumerate(s):
            try:
                if self.generator[i] != ch:
                    return False
            except IndexError:
                return False
        return True



if __name__ == '__main__':
    qapp = QApplication(sys.argv)
    window = LoginPage()
    window.show()
    sys.exit(qapp.exec())

