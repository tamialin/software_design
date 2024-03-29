from flask import request, redirect, url_for, render_template

def profileU():
    if request.method == 'POST':
        fullname = request.form['fullname']
        address1 = request.form['address1']
        address2 = request.form['address2']
        city = request.form['city']
        states = request.form['states']
        zip = request.form['zip']

        # Check if input is correct
        if fullname =="" or address1=="" or city=="" or states=="" or zip=="":
            error_message = "Please fill out empty fields"
            return render_template('ProfileManage.html', error_message=error_message)
        else:
            return redirect(url_for('history'))
    return render_template('ProfileManage.html')
    #return render_template('quote.html')
