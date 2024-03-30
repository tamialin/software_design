from flask import request, redirect, url_for, render_template, Flask, session

def profileU():
    if request.method == 'POST':
        fullname = request.form['fullname']
        address1 = request.form['address1']
        address2 = request.form['address2']
        city = request.form['city']
        states = request.form['states']
        zip = request.form['zip']

        # Check if input is correct
        if fullname == "" or address1 == "" or city == "" or states == "" or zip == "":
            error_message = "Please fill out empty fields"
            return render_template('ProfileManage.html', error_message=error_message)
    # if GET 
    return render_template('ProfileManage.html', fullname = fullname, address1=address1, address2=address2, city = city, states = states, zip = zip)