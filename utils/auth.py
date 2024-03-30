from flask import request, redirect, url_for, render_template, session
from utils.temp_db import users_db

def handle_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username exists and the password is correct
        if username in users_db and users_db[username]['password'] == password:
            session["username"] = username
            return redirect(url_for('home'))
        else:
            error_message = "Invalid username or password. Please try again."
            return render_template('Login.html', error_message=error_message)
    return render_template('Login.html')
