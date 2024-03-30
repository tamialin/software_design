from flask import request, redirect, url_for, render_template, Flask, session
from utils.temp_db import users_db

def profileU():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login page if user is not logged in

    username = session.get("username")
    user_info = users_db.get(username)

    if request.method == 'POST':
        fullname = request.form['fullname']
        address1 = request.form['address1']
        address2 = request.form['address2']
        city = request.form['city']
        states = request.form['states']
        zip_code = request.form['zip']

        # Update user info in database
        users_db[username]['fullName'] = fullname
        users_db[username]['address'] = address1
        users_db[username]['address2'] = address2
        users_db[username]['city'] = city
        users_db[username]['state'] = states
        users_db[username]['zipCode'] = zip_code

        return redirect(url_for('profile'))  # Redirect to profile page or wherever appropriate

    # Pass user_info to the template for displaying initial values
    return render_template('profileManage.html', user_info=user_info)
