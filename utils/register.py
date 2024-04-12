from flask import request, render_template, jsonify, session
import time, hashlib

def register_user(mysql):
    username = request.form['username']
    password = request.form['password']
    repassword = request.form['re-password']
    
    if repassword != password:
        message = 'Password and Re-enter Password must be the same'
        return render_template('register.html', error_message=message)
    
    # Check if user already exists
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    
    if user:
        message = 'Username already exists.'
        return render_template('register.html', error_message=message)
    
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    # Insert new user into the database
    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
    mysql.connection.commit()
    cur.close()
    
    message = 'User registered successfully!'
    session["username"] = username
    return render_template('register.html', success_message=message)
