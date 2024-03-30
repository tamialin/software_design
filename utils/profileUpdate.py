from flask import request, redirect, url_for, render_template, Flask, session
from utils.temp_db import users_db

#users = {
#    'user1': {'username' : 'user1', 'fullname': 'Heidar here', 'address1': '1314', 'address2': 'shadowbrook', 'city': 'Houston', 'states': 'CA', 'zip': '12345'}
#}

def profileU():
    #username = 'user1'
    #user_data = users.get(username, {})

    if 'username' not in session:
        return redirect(url_for('login'))

    username = session.get("username")
    user_data = users_db.get(username, {})

    if request.method == 'POST':
        users_db [username]= {
        'username' : username,
        'fullname' : request.form['fullname'], 
        'address1' : request.form['address1'],
        'address2' : request.form.get('address2', ''),
        'city' : request.form['city'],
        'states' : request.form['states'],
        'zip' : request.form['zip'],
        }
        
        return redirect(url_for('home'))
        #return "Profile updated successfully"

    return render_template('ProfileManage.html', user_data=user_data)