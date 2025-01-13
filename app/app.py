from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
from config import config
import calendar
import db

db.create_db()

app=Flask(__name__)

csrf = CSRFProtect() 
login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return db.get_by_id(db, id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = db.User(0, request.form['user'], request.form['pass'])
        logged_user = db.login(db, user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash("Invalid password...")
                return render_template('login.html')
        else:
            flash("User not found...")
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
def index():
    query = request.args.get('query','')
    if query:
        frontquery=db.search_data(query)
    else:
        frontquery=db.query()
    return render_template('index.html', frontquery=frontquery)

@app.route('/calendario/<int:year>/<int:month>')
def calendario(year, month):
    # Crear el calendario para el mes y año dados
    cal = calendar.Calendar()
    month_days = cal.monthdayscalendar(year, month)

    # Nombres de los días de la semana
    day_names = list(calendar.day_name)

    return render_template('cal.html', month=month, year=year, days=month_days, day_names=day_names)

@app.route('/insert', methods=['GET', 'POST'])
@login_required
def insert():
    if request.method == 'POST':
        # recibe datos del formulario
        ext = request.form['ext']
        user = request.form['user']
        mail = request.form['mail']
        phone = request.form['phone']
        site = request.form['site']
        department = request.form['department']
        db.create_data(ext, user, mail, phone, site, department)
        return redirect(url_for('insert'))
    frontquery=db.query()
    return render_template('crud/insert.html', frontquery=frontquery)

@app.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    if request.method == 'POST':
        selected_exts = request.form.getlist('ext')
        for ext in selected_exts:
            user = request.form.get(f'user_{ext}')
            mail = request.form.get(f'mail_{ext}')
            phone = request.form.get(f'phone_{ext}')
            site = request.form.get(f'site_{ext}')
            department = request.form.get(f'department_{ext}')
            db.update_data(user, mail, phone, site, department, ext)
        return redirect(url_for('update'))

    query = request.args.get('query', '')
    frontquery = db.search_data(query) if query else db.query()
    return render_template('crud/update.html', frontquery=frontquery)

@app.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    if request.method=='POST':
        ex=request.form.getlist('ext')
        db.delete_data(ex)
        return redirect(url_for('delete'))
    query = request.args.get('query','')
    if query:
        frontquery=db.search_data(query)
    else:
        frontquery=db.query()
    return render_template('crud/delete.html', frontquery=frontquery)

def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrada</h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['dev'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run(host='0.0.0.0', port='5500')