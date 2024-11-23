from flask import Flask, render_template, request, redirect, url_for
import db

db.create_db()

app=Flask(__name__)

@app.route('/')
def index():
    frontquery=db.query()
    return render_template('index.html', frontquery=frontquery)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/test1')
def test1():
    return render_template('test1.html')

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        # recibe datos del formulario
        ext = request.form['ext']
        user = request.form['user']
        mail = request.form['mail']
        phone = request.form['phone']
        # insercion en la BD
        db.create_data(ext, user, mail, phone)
        return redirect(url_for('insert'))
    frontquery=db.query()
    return render_template('crud/insert.html', frontquery=frontquery)

@app.route('/update')
def update():
    frontquery=db.query()
    return render_template('crud/update.html', frontquery=frontquery)

@app.route('/delete')
def delete():
    frontquery=db.query()
    return render_template('crud/delete.html', frontquery=frontquery)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')