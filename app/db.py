# app/db.py
import pandas as pd
import sqlite3

db = 'contacts.db'

def get_conn():
    return sqlite3.connect(db)

def create_db():
    with get_conn() as con:
        cur = con.cursor()
        cur.execute(''' 
            create table if not exists contacts(
            id integer primary key autoincrement, 
            user text not null,
            mail text not null,
            assigned_number text, 
            ext num)''')
        cur.execute("select count(*) from contacts")
        res=cur.fetchone()
        if res is not None:
            if res[0]==0:
                df = pd.read_csv('agenda.csv')
                if 'id' in df.columns:
                    df = df.drop(columns=['id'])
                columns_to_insert = ['user', 'mail', 'assigned_number', 'ext']
                df.to_sql('contacts', con, if_exists='append', index=False)

def query():
    with get_conn() as con:
        cur = con.cursor()
        cur.execute("Select * from contacts")
        total = cur.fetchall()
    return total

