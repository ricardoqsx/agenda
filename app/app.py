from flask import Flask, render_template, request, redirect, url_for
import db

db.create_db()

app=Flask(__name__)

@app.route('/')
def index():
    dbquery=db.query()
    return render_template('index.html', dbquery=dbquery)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/test1')
def test1():
    return render_template('test1.html')

@app.route('/insert')
def insert():
    dbquery=db.query()
    return render_template('crud/insert.html', dbquery=dbquery)

@app.route('/update')
def update():
    dbquery=db.query()
    return render_template('crud/update.html', dbquery=dbquery)

@app.route('/delete')
def delete():
    dbquery=db.query()
    return render_template('crud/delete.html', dbquery=dbquery)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')