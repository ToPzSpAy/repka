import os
import shutil

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QGraphicsScene, QMessageBox, QWidget, QLabel, \
    QListWidgetItem, QStackedWidget, QLineEdit, QListWidget, QFileDialog
from PyQt5 import uic
import sys
from sql import SqlDB
import cloud_storage
import logging

class AuthWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("auth.ui", self)
        self.conf_btn.clicked.connect(self.login)
        self.reg_btn.clicked.connect(self.signin_page)
        self.back_btn.clicked.connect(self.back_page)
        self.create_btn.clicked.connect(self.signin)
        self.img_btn.clicked.connect(self.img_select)
        self.mysql = SqlDB()

    def login(self):
        res, you = self.mysql.load(self)
        if res:
            self.ui = Appw(you)
            self.ui.show()
            self.close()

    def signin_page(self):
        self.stackedWidget.setCurrentWidget(self.page_2)

    def back_page(self):
        self.stackedWidget.setCurrentWidget(self.page_1)

    def img_select(self):
        self.path, _ = QFileDialog.getOpenFileName(self, 'Выберите файл', '', "Изображение (*.png, *.jpg);;All Files (*)")
        print(self.path)
        self.pix = QPixmap(self.path)
        self.pix = self.pix.scaled(self.img_fr.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.img_fr.setPixmap(self.pix)


    def signin(self):
        img = ''
        if self.path:
            img = cloud_storage.upload(self.path)
        params = (self.login_line1.text(), self.pass_line2.text())
        params2 = (self.name_line.text(), self.name2_line.text(), self.about_line.text(), img)
        self.mysql.create(params, params2)
        QMessageBox.about(self, "Готово", "Аккаунт создан!")
        self.stackedWidget.setCurrentWidget(self.page_1)


class Appw(QWidget):
    def __init__(self, you):
        super().__init__()
        uic.loadUi("gui.ui", self)
        self.usr = you
        self.current_row = 0
        self.edit_btn.clicked.connect(self.edit_page)
        self.editconf_btn.clicked.connect(self.edit_ur_data)
        self.back_btn.clicked.connect(self.back_page)
        self.delacc_btn.clicked.connect(self.delacc)
        self.mysql = SqlDB()
        self.user_list()

    def user_list(self):
        self.list.clear()
        self.usrdata = self.mysql.select()
        for user in self.usrdata:
            item = QListWidgetItem(user[1])
            self.list.insertItem(self.current_row, item)
            self.current_row += 1
        self.list.itemClicked.connect(self.user_info)

    def user_info(self,item):
        self.cuser = []
        for user in self.usrdata:
            if user[1] == item.text():
                self.cuser = user
                break
        if self.usr[3] >= 1:
            self.label_1.setText('Ник: ' + self.cuser[1])
            self.label_2.setText('' + self.cuser[5] + ' ' + self.cuser[6])
            self.label_3.setText('Инфо: ' + self.cuser[7])

            self.pix = QPixmap()
            self.pix.loadFromData(cloud_storage.load(self.cuser[8]))
            self.pix = self.pix.scaled(self.img_prof.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.img_prof.setPixmap(self.pix)

    def edit_ur_data(self):
        if self.usr[3] >= 2:
            self.mysql.edit(self, self.cuser[0])
        else:
            self.mysql.edit(self, self.usr[0])
        tusr = self.mysql.user_data(self.usr[1])
        if self.usr != tusr:
            self.usr = tusr
        self.user_list()

    def delacc(self):
        ret = QMessageBox.question(self, 'Удаление', 'Точно-точно хотите удалить?',
                                   QMessageBox.Yes | QMessageBox.No)
        if ret == QMessageBox.Yes:
            if self.usr[3] >= 2:
                self.mysql.delete(self.cuser)
                self.user_list()
            else:
                self.mysql.delete(self.usr)
                self.w = AuthWindow()
                self.w.show()
                self.close()

    def edit_page(self):
        self.stackedWidget.setCurrentWidget(self.page_edit)
        if self.usr[3] >= 2:
            self.pass_line.setText(self.cuser[2])
            self.name_line.setText(self.cuser[5])
            self.name2_line.setText(self.cuser[6])
            self.about_line.setText(self.cuser[7])
            self.lvl_line.setValue(self.cuser[3])
            self.lvl_line.setEnabled(True)
        else:
            self.pass_line.setText(self.usr[2])
            self.name_line.setText(self.usr[5])
            self.name2_line.setText(self.usr[6])
            self.about_line.setText(self.usr[7])
            self.lvl_line.setValue(self.usr[3])



    def back_page(self):
        self.stackedWidget.setCurrentWidget(self.page_users)

if __name__ == '__main__':
        qapp = QApplication(sys.argv)
        window = AuthWindow()
        window.show()
        qapp.exec()
#        encryption('data.db', 'lokol123123')

