from flask import Flask, render_template, url_for, session, redirect, request
from flask_session import Session
from utils.auth import handle_login
from utils.profileUpdate import profileU
from utils.fuelModule import fuelQuote

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

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
    return fuelQuote()
    # return render_template('quote.html')

@app.route('/history')
def history():
    if not session.get("username"):
        return redirect("/login")
    return render_template('history.html')

@app.route('/profile', methods=["POST", "GET"])
def profile():

    return profileU()
    # return render_template('ProfileManage.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    return handle_login()

@app.route('/logout')
def logout():
    session["username"] = None
    return redirect("/")

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('Register.html')

if __name__ == '__main__':
    app.run(debug=True)