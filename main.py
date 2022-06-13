import base64
import os
import random
import shutil
from datetime import datetime

from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QGraphicsScene, QMessageBox, QWidget, QLabel, \
    QListWidgetItem, QStackedWidget, QLineEdit, QListWidget, QFileDialog, QTableWidgetItem, QHeaderView, QCompleter, \
    QComboBox, QVBoxLayout, QDateEdit
from PyQt5 import uic, QtCore
import sys
import pdf_m
from capcha import CapthaController, Captha
from sql import SqlDB
from pdf_m import barcode_pdf
import logging

class AuthWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("auth.ui", self)
        self.attempts = 0
        self.conf_btn.clicked.connect(self.login)
        self.img_btn.clicked.connect(self.img_select)
        self.swps_chk.clicked.connect(self.pass_show)
        self.controller = CapthaController()
        self.captha_widget = Captha(self.controller)
        self.captha_line = QLineEdit()

    def login(self):
        cap = True
        if self.attempts > 1:
            self.captha_layout.addWidget(self.captha_widget)
            self.captha_layout.addWidget(self.captha_line)
            cap = self.controller.check_captcha(self.captha_line.text())

        if cap:
            self.mysql = SqlDB()
            res, you = self.mysql.load(self)
            if res:
                self.ui = Appw(you,self.mysql)
                self.ui.show()
                self.close()
        else:
            self.label_3.setText('Капча не верна')
        self.attempts += 1
        self.captha_widget.update_value()

    def pass_show(self):
        if self.swps_chk.isChecked():
            self.pass_line.setEchoMode(QLineEdit.Normal)
        else:
            self.pass_line.setEchoMode(QLineEdit.Password)




    def img_select(self):
        self.path, _ = QFileDialog.getOpenFileName(self, 'Выберите файл', '', "Изображение (*.png, *.jpg);;All Files (*)")
        print(self.path)
        self.pix = QPixmap(self.path)
        self.pix = self.pix.scaled(self.img_fr.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.img_fr.setPixmap(self.pix)


    # def signin(self):
    #     img = ''
    #     if self.path:
    #         img = cloud_storage.upload(self.path)
    #     params = (self.login_line1.text(), self.pass_line2.text())
    #     params2 = (self.name_line.text(), self.name2_line.text(), self.about_line.text(), img)
    #     self.mysql.create(params, params2)
    #     QMessageBox.about(self, "Готово", "Аккаунт создан!")
    #     self.stackedWidget.setCurrentWidget(self.page_1)


class Appw(QWidget):
    def __init__(self, you,mysql):
        super().__init__()
        uic.loadUi("gui.ui", self)
        self.mysql = mysql
        self.usr = you
        self.current_row = 0
        self.services=[]

        self.editconf_btn.clicked.connect(self.edit_ur_data)
        self.back_btn.clicked.connect(self.back_page)
        self.back_btn2.clicked.connect(self.back_page)
        self.delacc_btn.clicked.connect(self.delacc)
        self.hist_btn.clicked.connect(self.history_page)
        self.filt_l_btn.clicked.connect(self.sort_login)
        self.ord_btn.clicked.connect(self.order_page)
        self.barcode_btn.clicked.connect(self.barcode_gen)
        self.makeorder_btn.clicked.connect(self.new_order)
        self.add_serv_btn.clicked.connect(self.add_service)
        self.back_btn3.clicked.connect(self.back_page)
        self.create_client_btn.clicked.connect(self.create_client)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.setInterval(1000)
        self.count = 0
        self.user_list()
        self.timer.start()

    def user_list(self):
        self.list.clear()
        self.usrdata = self.mysql.select()
        for user in self.usrdata:
            item = QListWidgetItem(user[2])
            self.list.insertItem(self.current_row, item)
            self.current_row += 1
        self.list.itemClicked.connect(self.user_info)

    def user_info(self,item):
        ind = self.list.currentRow()
        self.cuser = self.usrdata[ind]
        self.label_1.setText('Ник: ' + self.cuser[3])
        self.label_2.setText(self.cuser[2])
        self.label_3.setText('Должность: ' + self.cuser[1])

        self.pix = QPixmap()
        self.pix.loadFromData(base64.b64decode(self.cuser[7]))
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


    def showTime(self):
        self.count += 1
        h = self.count // 3600
        m = self.count % 3600 // 60
        s = self.count % (3600 * 60) % 60
        time = f"{h}:{m}:{s}"
        if self.count >= 8100:
            time += f"  Через {30-m} минут завершится сеанс"
        self.time_lb.setText(time)
        if self.count >= 9000:
            self.exit_acc()

    def back_page(self):
        self.stackedWidget.setCurrentWidget(self.page_users)
#               Оформление зака

    def order_page(self):
        self.stackedWidget.setCurrentWidget(self.page_order)

        self.services = []
        self.serv_sum = 0
        self.usluga_id = ''
        orders_list = self.mysql.select_orders()
        ListOfCode = [c[1] for c in orders_list]
        self.hint = str(max(ListOfCode)+1)
        comp = QCompleter([self.hint], self.ordnum_line)
        self.ordnum_line.setCompleter(comp)
        self.ordnum_line.setPlaceholderText(self.hint)
        self.date_Lb.setText(datetime.today().date().strftime("Дата: %d.%m.%Y"))

        self.clients_list = self.mysql.select_clients()
        names = [n[0] for n in self.clients_list]
        self.client_cbx.clear()
        self.client_cbx.addItems(names)
        comp = QCompleter(names, self.client_cbx)
        self.client_cbx.setCompleter(comp)

        self.serv_list = self.mysql.select_services()
        serv_names = [n[1] for n in self.serv_list]
        self.usluga_cbx.clear()
        self.usluga_cbx.addItems(serv_names)
        comp = QCompleter(serv_names, self.usluga_cbx)
        self.usluga_cbx.setCompleter(comp)

    def barcode_gen(self):
        id = self.ordnum_line.text()
        today = datetime.today()
        date = today.strftime("%d%m%Y%H%M")
        code = str(random.randint(1,999999))
        while len(code)<6:
            code = '0'+code
        bc = id+date+code
        print(bc)
        barcode_pdf(bc)

    def new_order(self):
        id = self.ordnum_line.text()
        cl = self.client_cbx.currentText()
        num_client = list(filter(lambda a: cl in a, self.clients_list))[0][1]
        srv = self.services
        dt = datetime.today().date().strftime("%d.%m.%Y")
        tm = datetime.today().time().strftime("%H:%M")
        sm = str(self.serv_sum)
        print(id,cl,srv,dt)
        pdf_m.order_pdf(id, cl, srv, dt, sm, num_client)

        order=[]
        order.append(id)
        order.append(dt)
        order.append(tm)
        order.append(str(num_client))
        order.append(self.usluga_id[:-2])
        self.mysql.insert_order(order)

        msg = QMessageBox()
        msg.setWindowTitle("Заказ")
        msg.setText("Заказ был создан")

        x = msg.exec_()



    def create_client(self):
        self.cw = NewClient(self)
        self.cw.show()

    def add_service(self):
        self.services.append(self.usluga_cbx.currentText())
        filter_object = filter(lambda a: self.usluga_cbx.currentText() in a, self.serv_list)
        cur_service = list(filter_object)[0]
        self.usluga_id += str(cur_service[0])+', '
        self.serv_sum += cur_service[3]
        self.sum_Lb.setText('Итог: '+str(self.serv_sum))
        txt = ""
        for srv in self.services:
            txt += srv + "\n"
        self.all_serv_l.setText(txt)




#           Иитория посика
    def history_page(self):
        self.stackedWidget.setCurrentWidget(self.page_history)

        self.his_users = self.mysql.select_history()
        y=0
        for us in self.his_users:
            self.table_his.insertRow(y)
            for x in range(3):
                self.table_his.setItem(y, x, QTableWidgetItem(us[x]))
            y += 1
        self.table_his.resizeRowsToContents()
    def sort_login(self):
        srtd_users = sorted(self.his_users, key=lambda login: login[0].lower())
        self.table_his.setRowCount(0)
        y = 0
        for us in srtd_users:
            self.table_his.insertRow(y)
            for x in range(3):
                self.table_his.setItem(y, x, QTableWidgetItem(us[x]))
            y += 1
        self.table_his.resizeRowsToContents()
    def sort_data(self):
        srtd_users = sorted(self.his_users, key=lambda login: datetime.strptime(login[1],"%d:%m:%Y %H:%M:%S"))
        self.table_his.setRowCount(0)
        y = 0
        for us in srtd_users:
            self.table_his.insertRow(y)
            for x in range(3):
                self.table_his.setItem(y, x, QTableWidgetItem(us[x]))
            y += 1


    def exit_acc(self):
        self.w = AuthWindow()
        self.w.show()
        self.close()

class NewClient(QWidget):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        uic.loadUi("client.ui", self)
        self.lineEdit_2.setText(self.ui.hint)
        self.create_btn.clicked.connect(self.create_client)

    def create_client(self):
        client = [self.lineEdit.text(), self.lineEdit_2.text(), self.lineEdit_3.text(),
                  self.dateEdit.text(), self.textEdit_5.toPlainText(), self.lineEdit_6.text(), self.lineEdit_7.text()]
        print(client)
        self.ui.mysql.insert_client(client)
        self.close()
        self.ui.order_page()
if __name__ == '__main__':
        qapp = QApplication(sys.argv)
        window = AuthWindow()
        window.show()
        qapp.exec()
#        encryption('data.db', 'lokol123123')

