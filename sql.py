import sqlite3
from crpypt import encryption, decryption
#from sqlcipher3 import dbapi2 as sqlcipher
class SqlDB:
    def clear(self):
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()

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
        conn.commit()
        conn.close()

    def create(self, params, params2):
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO users VALUES(NULL, ?, ?, 1)", params)
        cur.execute("INSERT INTO users_info VALUES(NULL, ?, ?, ?, ?)", params2)
        conn.commit()
        conn.close()

    def load(self, ui):
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM users, users_info WHERE users.id = users_info.id_inf")
        kok = cur.fetchall()
        conn.close()
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
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM users, users_info WHERE users.id = users_info.id_inf")
        usdata = cur.fetchall()
        conn.close()
        return usdata

    def edit(self, ui, login):
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        cur.execute(f"""UPDATE users SET pass = '{ui.pass_line.text()}', lvl = {str(ui.lvl_line.value())} WHERE id = {login};""")
        cur.execute(f"""UPDATE users_info SET name = '{ui.name_line.text()}',
                                              about = '{ui.about_line.toPlainText()}',
                                              second_name = '{ui.name2_line.text()}'
                                              WHERE id_inf = {login};""")
        # cur.execute(f"SELECT * FROM users, users_info WHERE users.id = users_info.id_inf AND users.id = {login}")
        # usr = cur.fetchone()
        conn.commit()
        conn.close()

    def delete(self, user):
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        cur.execute(f"""DELETE FROM users_info WHERE id_inf = {user[0]};""")
        cur.execute(f"""DELETE FROM users WHERE id = {user[0]}""")
        conn.commit()
        conn.close()

    def superuser(self, user_id):
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        cur.execute(f"""UPDATE users SET lvl = 2 WHERE id = {user_id};""")
        conn.commit()
        conn.close()

    def user_data(self, login):
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM users, users_info WHERE users.id = users_info.id_inf AND users.login = '{login}'")
        usr = cur.fetchone()
        conn.commit()
        conn.close()
        return usr


if __name__ == "__main__":
    SqlDB().clear()