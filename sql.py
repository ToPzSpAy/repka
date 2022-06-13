import sqlite3
import pymysql
#from sqlcipher3 import dbapi2 as sqlcipher


class SqlDB:
    def __init__(self):
        self.no_connection = False
        try:
            self.conn = pymysql.connect(
                host='sql11.freesqldatabase.com',
                port=3306,
                user='sql11498644',
                password='VJqqGd9LT7',
                database='sql11498644'
            )
            
            print('Ого заработало')
        except Exception as err:
            print('Чот неверно или не робит', err)
            self.no_connection = True

    def clear(self):
        cur = self.conn.cursor()

        cur.execute("""DROP TABLE IF EXISTS users;""")
        cur.execute("""CREATE TABLE users(
           id INTEGER PRIMARY KEY,
           login TEXT,
           pass TEXT,
           lvl INT);
        """)
        cur.execute("""DROP TABLE IF EXISTS users_info;""")
        cur.execute("""CREATE TABLE users_info(id_inf INTEGER PRIMARY KEY UNIQUE REFERENCES users(id),
                        name TEXT,
                        second_name TEXT,
                        about TEXT,
                        photo TEXT);
        """)
        self.conn.commit()

    def create(self, params, params2):
        cur = self.conn.cursor()
        cur.execute(f"INSERT INTO users(login, pass, lvl) VALUES(%s, %s, 1)", params)
        cur.execute(f"INSERT INTO users_info(name, second_name, about, photo) VALUES(%s, %s, %s, %s)", params2)
        self.conn.commit()

    def load(self, ui):
        if self.no_connection:
            ui.label_3.setText('Не удаётся подключиться \nк серверу')
            return False, None

        cur = self.conn.cursor()
        cur.execute("SELECT * FROM `Cотрудники`")
        kok = cur.fetchall()
        for user in kok:
            us = user[3]
            ps = user[4]
            if us == ui.login_line.text() and ps == ui.pass_line.text():
                ui.label_3.setText('Верно')
                return True, user
            else: ui.label_3.setText('Не правильно')
        return False, None

    def save_pic(self):
        import base64
        id = 'ID 110'
        image = open('avatars/Смирнова.jpeg', 'rb')  # open binary file in read mode
        image_read = image.read()
        image_64_encode = base64.b64encode(image_read)
        print(image_64_encode)
        cur = self.conn.cursor()
        image_64 = self.conn.escape_string(str(image_64_encode)[2:-1])
        cur.execute(f"UPDATE `Cотрудники` SET `Фото` = '{image_64}' WHERE `Код сотрудника` = '{id}';")
        self.conn.commit()

    def select(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM `Cотрудники`")
        usdata = cur.fetchall()
        return usdata

    def select_history(self):
        cur = self.conn.cursor()
        cur.execute("SELECT `Логин`, `Последний вход`, `Тип входа` FROM `Cотрудники`")
        usdata = cur.fetchall()
        return usdata

    def insert_client(self,data):
        cur = self.conn.cursor()
        cur.execute(f"INSERT INTO `Клиенты` VALUES (%s,%s,%s,%s,%s,%s,%s)", data)
        self.conn.commit()

    def select_clients(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM `Клиенты`")
        usdata = cur.fetchall()
        return usdata

    def select_orders(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM `Заказы`")
        usdata = cur.fetchall()
        return usdata

    def select_services(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM `Услуги`")
        data = cur.fetchall()
        return data

    def query(self):
        cur = self.conn.cursor()
        #cur.execute("DELETE FROM `Заказы` WHERE `Код заказа` = 100051")
        print(cur.rowcount)

    def insert_order(self,data):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM `Заказы`")
        idx = str(cur.rowcount + 1)
        cur.execute(f"INSERT INTO `Заказы` VALUES ({idx},%s,%s,%s,%s,%s,'Новая','','2 часа')", data)
        self.conn.commit()

    # def edit(self, ui, login):
    #     cur = self.conn.cursor()
    #     cur.execute(f"""UPDATE users SET pass = '{ui.pass_line.text()}', lvl = {str(ui.lvl_line.value())} WHERE id = {login};""")
    #     cur.execute(f"""UPDATE users_info SET name = '{ui.name_line.text()}',
    #                                           about = '{ui.about_line.toPlainText()}',
    #                                           second_name = '{ui.name2_line.text()}'
    #                                           WHERE id_inf = {login};""")
    #     # cur.execute(f"SELECT * FROM users, users_info WHERE users.id = users_info.id_inf AND users.id = {login}")
    #     # usr = cur.fetchone()
    #     self.conn.commit()



if __name__ == "__main__":
    oki = SqlDB()
    oki.query()