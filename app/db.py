# app/db.py
import pandas as pd
import sqlite3
from User import User

# users table operations

usrdb = 'users.db'

def conn_usr():
    return sqlite3.connect(usrdb)

def create_users():
    with conn_usr() as users:
        cur = users.cursor()
        cur.execute('''
            create table if not exists users(
            id integer primary key autoincrement,
            username text not null,
            password text not null,
            fullname text not null)''')
        cur.execute("select count(*) from users")
        rs=cur.fetchone()
        if rs is not None:
            if rs[0]==0:
                user_create = "insert into users (username, password, fullname) values (?, ?, ?)"
                # usuario de prueba
                username = "test"
                password = "scrypt:32768:8:1$uvmv05ggdxjtJmfp$scrypt:32768:8:1$VZCDJmJLswoxjFV9$507dada3f16d5de94367d986658942ea9be4d0ffae8932eeb513749b69286e6bd436bed73df9b9dc4a9577cdf3cb635a1ee3d0f019ebef5450a2083c605c8595"
                fullname = "Testing User"
                cur.execute(user_create,(username, password, fullname))


def login(user):
    with conn_usr() as users:
        cur = users.cursor()
        sql = """SELECT id, username, password, fullname FROM users 
                WHERE username = '{}'""".format(user.username)
        cur.execute(sql)
        row = cur.fetchone()
        if row != None:
            user = User(row[0], row[1], User.check_password(row[2], user.password), row[3])
            return user
        else:
            return None

def get_by_id(id):
    with conn_usr() as users:
        cur = users.cursor()
        sql = "SELECT id, username, fullname FROM users WHERE id = {}".format(id)
        cur.execute(sql)
        row = cur.fetchone()
        if row != None:
            return User(row[0], row[1], None, row[2])
        else:
            return None


# //////////////////////////////////////////////////////////////////////////////////////////////
# CRUD operations //////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////

contacts_db = 'contacts.db'

def get_conn():
    return sqlite3.connect(contacts_db)

def create_db():
    with get_conn() as con:
        cur = con.cursor()
        cur.execute(''' 
            create table if not exists contacts(
            ext integer primary key, 
            user text not null,
            mail text not null,
            phone text not null,
            site text not null,
            department text not null)''')
        cur.execute("select count(*) from contacts")
        res=cur.fetchone()
        if res is not None:
            if res[0]==0:
                df = pd.read_csv('agenda.csv')
                columns_to_insert = [ 'ext', 'user', 'mail', 'phone', 'site', 'department']
                df.to_sql('contacts', con, if_exists='append', index=False)

def query():
    with get_conn() as con:
        cur = con.cursor()
        cur.execute("Select * from contacts order by user asc")
        total = cur.fetchall()
    return total

def search_data(val):
    with get_conn() as con:
        cur = con.cursor()
        cur.execute("select * from contacts where user like ?",('%'+val+'%',))
        total = cur.fetchall()
    return total

def dep_data():
    with get_conn() as con:
        cur = con.cursor()
        cur.execute("select departments from contacts")
        total = cur.fetchall()
    return total

def create_data(ex,us,ma,ph,st,dp):
    with get_conn() as con:
        cur = con.cursor()
        inser_data= "insert into contacts (ext, user, mail, phone, site, department) values (?, ?, ?, ?, ?, ?)"
        cur.execute(inser_data,(ex, us, ma, ph, st, dp))

def update_data(us, ma, ph, st, dp, ex):
    with get_conn() as con:
        cur = con.cursor()
        upd = ''' update contacts 
                    set user =?, 
                    mail = ?, 
                    phone = ?,
                    site = ?,
                    department = ? 
                  where ext = ?
              '''
        cur.execute(upd,(us, ma, ph, st, dp, ex))

def delete_data(ex):
    with get_conn() as con:
        cur = con.cursor()
        for ext in ex:
            cur.execute("delete from contacts where ext = ?", (ext,))

# anotacion sobre for
# en la funcion, ex funciona como una lista 
# que va tomando los datos en la lista (que tiene ex) 
# y le va pasando a ext y entonces 
# el valor de ext se le va pasando al query

