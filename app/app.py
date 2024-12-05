from flask import Flask, render_template, request, redirect, url_for
import db

db.create_db()

app=Flask(__name__)

@app.route('/')
def index():
    query = request.args.get('query','')
    if query:
        frontquery=db.search_data(query)
    else:
        frontquery=db.query()
    return render_template('index.html', frontquery=frontquery)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/test1')
# esto es un playground para pruebas
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
        db.create_data(ext, user, mail, phone)
        return redirect(url_for('insert'))
    frontquery=db.query()
    return render_template('crud/insert.html', frontquery=frontquery)

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        selected_exts = request.form.getlist('ext')
        for ext in selected_exts:
            user = request.form.get(f'user_{ext}')
            mail = request.form.get(f'mail_{ext}')
            phone = request.form.get(f'phone_{ext}')
            db.update_data(user, mail, phone, ext)
        return redirect(url_for('update'))

    query = request.args.get('query', '')
    frontquery = db.search_data(query) if query else db.query()
    return render_template('crud/update.html', frontquery=frontquery)

@app.route('/delete', methods=['GET', 'POST'])
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')