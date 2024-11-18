from flask import Flask, render_template, request, redirect, url_for
import db

db.create_db()

app=Flask(__name__)

@app.route('/')
def index():
    dbquery=db.query()
    return render_template('index.html', dbquery=dbquery)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')