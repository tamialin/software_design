from flask import request, redirect, url_for, render_template, Flask, session
from utils.temp_db import users_db

def profileU(mysql):

    if 'username' not in session:
        return redirect(url_for('login'))

    username = session.get("username")
    password = session.get("password")

    dbInfo = mysql.connection.cursor()
    dbInfo.execute("SELECT * FROM users WHERE username = %s", (username, ))
    user_data = dbInfo.fetchone()

    if request.method == 'POST':
        fullname = request.form['fullname']
        address1 = request.form['address1']
        address2 = request.form.get('address2', '')
        city = request.form['city']
        states = request.form['states']
        zip = request.form['zip']

        dbInfo.execute("UPDATE users SET fullname = %s, address1 = %s, address2 = %s, city = %s, states = %s, zip = %s WHERE username = %s", (fullname, address1, address2, city, states, zip, username))
        mysql.connection.commit()
        dbInfo.close()

        return redirect(url_for('profile'))
        #return "Profile updated successfully"
    else :
        print("get database data:\n", user_data)
    
    # preview data
    user_info = {
            'username' : user_data[0] if user_data else username,
            'password' : user_data[1] if user_data else password,
            'fullname' : user_data[2] if user_data else "no data",
            'address1' : user_data[3] if user_data else "no data",
            'address2' : user_data[4] if user_data else "no data",
            'city' : user_data[5] if user_data else "no data",
            'states' : user_data[6] if user_data else "no data",
            'zip' : user_data[7] if user_data else "no data"
    }
    return render_template('ProfileManage.html', user_data=user_info)