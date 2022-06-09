import sqlite3
import pymysql
#from sqlcipher3 import dbapi2 as sqlcipher


class SqlDB:
    def __init__(self):
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
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM users, users_info WHERE users.id = users_info.id_inf")
        kok = cur.fetchall()
        print(kok)
        for user in kok:
            us = user[1]
            ps = user[2]
            if us == ui.login_line.text() and ps == ui.pass_line.text():
                ui.label_3.setText('Верно')
                return True, user
            else: ui.label_3.setText('Не правильно')
        return False, None

    def select(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM users, users_info WHERE users.id = users_info.id_inf")
        usdata = cur.fetchall()
        return usdata

    def edit(self, ui, login):
        cur = self.conn.cursor()
        cur.execute(f"""UPDATE users SET pass = '{ui.pass_line.text()}', lvl = {str(ui.lvl_line.value())} WHERE id = {login};""")
        cur.execute(f"""UPDATE users_info SET name = '{ui.name_line.text()}',
                                              about = '{ui.about_line.toPlainText()}',
                                              second_name = '{ui.name2_line.text()}'
                                              WHERE id_inf = {login};""")
        # cur.execute(f"SELECT * FROM users, users_info WHERE users.id = users_info.id_inf AND users.id = {login}")
        # usr = cur.fetchone()
        self.conn.commit()

    def delete(self, user):
        cur = self.conn.cursor()
        cur.execute(f"""DELETE FROM users_info WHERE id_inf = {user[0]};""")
        cur.execute(f"""DELETE FROM users WHERE id = {user[0]}""")
        self.conn.commit()

    def superuser(self, user_id):
        cur = self.conn.cursor()
        cur.execute(f"""UPDATE users SET lvl = 2 WHERE id = {user_id};""")
        self.conn.commit()

    def user_data(self, login):
        cur = self.conn.cursor()
        cur.execute(f"SELECT * FROM users, users_info WHERE users.id = users_info.id_inf AND users.login = '{login}'")
        usr = cur.fetchone()
        self.conn.commit()
        return usr


if __name__ == "__main__":
    oki = SqlDB()
    oki.clear()
