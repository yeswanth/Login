from flask import Flask, render_template, request, session, g, flash, redirect
from flask_login import login_user, logout_user, LoginManager
from contextlib import closing
import sqlite3



#configuration 
DATABASE = '/tmp/login_system.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


app = Flask(__name__)
app.config.from_object(__name__)
login_manager = LoginManager()


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def initdb():
    with closing(connect_db()) as db:
         with app.open_resource('schema.sql') as f:
              db.cursor().executescript(f.read())
         db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

#@app.after_request
def teardown_request(exception):
    g.db.close()

def validate_cred(email, password):
    cur = g.db.execute('select email, password from logincred order by id')
    entries = [dict(email=row[0], pwd=row[1]) for row in cur.fetchall()]
    for entry in entries:
        if entry['email'] == email and entry['pwd'] == password:
            return True

    return False

def add_entry(fname, lname, email, password):
    flash('abcde')
    cur = g.db.execute('insert into logincred (fname, lname, email, password) values (?, ?, ?, ?)', (fname, lname, email, password))
    g.db.commit()
    flash('New entry has been created')


@app.route("/")
def index():
    return "Hello World"

@app.route("/register", methods=['GET','POST'])
def register():
    if request.method == 'POST':
         add_entry(request.form['fname'], request.form['lname'], 
                   request.form['email'], request.form['password'])     
         return redirect('register-true')
    else:
        return render_template("register.html")

@login_manager.user_loader
def load_user(userid):
    return User.get(userid)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
       if validate_cred(request.form['email'], request.form['password']):
            return redirect("/")
       else:
            return render_template("login.html", error="Wrong credentials")
    else:
        return render_template("login.html")


@app.route("/register-true", methods=['GET','POST'])
def register_success():
    return "Registration successful. Thank You!!!"



if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
