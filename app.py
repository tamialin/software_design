from flask import Flask, render_template, url_for, session, redirect, request
from flask_session import Session
from flask_mysqldb import MySQL
from flask import jsonify


from utils.auth import handle_login
from utils.profileUpdate import profileU
from utils.fuelModule import fuelQuote
from utils.history import get_quote_history
from utils.register import register_user

app = Flask(__name__)
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'our_users'

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/quote', methods=["POST", "GET"])
def quote():
    if not session.get("username"):
        return redirect("/login")
    return fuelQuote(mysql)

@app.route('/history')
def history():
    if not session.get("username"):
        return redirect("/login")
    username = session.get('username') 
    quote_history = get_quote_history(username, mysql)
    return render_template('history.html', quote_history=quote_history)

@app.route('/profile', methods=["POST", "GET"])
def profile():
    if not session.get("username"):
        return redirect("/login")
    return profileU(mysql)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('Login.html')
    if request.method == 'POST':
        return handle_login(mysql)


@app.route('/logout')
def logout():
    session["username"] = None
    return redirect("/")

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        return register_user(mysql)

if __name__ == '__main__':
    app.run(debug=True)