from flask import request, render_template
import time, hashlib

def register_user(mysql):
    username = request.form['username']
    password = request.form['password']
    
    # Check if user already exists
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    
    if user:
        message = 'Username already exists.'
        time.sleep(3)
        return render_template('register.html', message=message)
    
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    # Insert new user into the database
    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
    mysql.connection.commit()
    cur.close()
    
    message = 'Register Successfully!'
    render_template('register.html', message=message)
    time.sleep(3)
    return render_template('login.html', message=message)
