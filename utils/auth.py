from flask import request, redirect, url_for, render_template, session
import hashlib


def handle_login(mysql, clickfrom):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Fetch user from MySQL database
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if hashed_password == user[1]:  # Access the password hash by index
                # Password is correct, set the session username
                session["username"] = username
                print(clickfrom)
                if clickfrom:
                    return redirect(url_for(clickfrom))
                else:
                    return redirect(url_for('home'))
            else:
                error_message = "Invalid username or password. Please try again."
                return render_template('Login.html', clickfrom=clickfrom, error_message=error_message)
        else:
            error_message = "Invalid username or password. Please try again."
            return render_template('Login.html', clickfrom=clickfrom, error_message=error_message)

    return render_template('Login.html', clickfrom=clickfrom)

