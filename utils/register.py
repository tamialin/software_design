# from flask import request, redirect, url_for, render_template, session

# # Hardcoded user credentials
# users = {'user1': 'password1', 'user2': 'password2'}

# def handle_login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         # Check if the username exists and the password is correct
#         if username in users and users[username] == password:
#             # Authentication successful, you can redirect to another page or perform additional actions
#             session["username"] = username
#             return redirect(url_for('home'))
#         else:
#             # Authentication failed, you can display an error message
#             error_message = "Invalid username or password. Please try again."
#             return render_template('Login.html', error_message=error_message)
#     return render_template('Login.html')
