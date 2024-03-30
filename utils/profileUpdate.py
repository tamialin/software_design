from flask import request, redirect, url_for, render_template, Flask, session

users = {
    'user1': {'fullname': 'Heidar here', 'address1': '1314', 'address2': 'shadowbrook', 'city': 'Houston', 'state': 'CA', 'zip': '12345'}
}

def profileU():
    if request.method == 'POST':
        username = 'user1'
        users [username]= {
        'fullname' : request.form['fullname'], 
        'address1' : request.form['address1'],
        'address2' : request.form['address2'],
        'city' : request.form['city'],
        'states' : request.form['states'],
        'zip' : request.form['zip'],
        }
        
        return redirect(url_for('home'))
        #return "Profile updated successfully"

    return render_template('ProfileManage.html')