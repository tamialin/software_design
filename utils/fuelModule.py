from flask import Flask, jsonify, request, redirect, url_for, render_template, session
from utils.pricing import FuelPricing
from utils.temp_db import users_db

def fuelQuote(mysql):
   username = session.get("username")
   cur = mysql.connection.cursor()

   #Get address from DB
   cur.execute("SELECT address1, city, states, zip, history from users WHERE username = %s", (username,))
   fetchValues = cur.fetchone()
   if fetchValues[0] != None:
      address = fetchValues[0]
      city = fetchValues[1]
      state = fetchValues[2]
      zipCode = fetchValues[3]
      dAddress  = f"{address}, {city}, {state}, {zipCode}"
      returnUser = fetchValues[4]
   else: 
      dAddress = "Address Hasn't Been Set Up. Please Update Your Profile"
   # print(state)
   
   # Receive input from quote page

   if request.method == 'POST':
      gallon = float(request.form["gallonsRequested"])
      date = request.form["deliveryDate"]
      pricingModule = FuelPricing()
      suggested_price, total_price = pricingModule.calculatingPrice(gallon, state, returnUser)

      # Return the value to display quote
      if 'displayData' in request.form:
         return jsonify(suggested_price = suggested_price, total_price = total_price)
      elif 'sendData' in request.form: # send user input and prices to history backend
         sendToDB(mysql, username, date, gallon, address, suggested_price, total_price)
         if returnUser == 0:
            cur.execute("UPDATE users SET history = %s WHERE username = %s", (1, username)) #Update user history factor
            mysql.connection.commit()
         cur.close()
         return jsonify(success = True)
   
   return render_template('quote.html', dAddress = dAddress)  

def sendToDB(mysql, username, date, gallon, address, suggested_price, total_price):
   username = session.get("username")
   cur = mysql.connection.cursor()
   cur.execute("SELECT * FROM users WHERE username = %s", (username,))
   user = cur.fetchone()

   cur.execute("INSERT INTO quote_history (username, date, gallon, address, price, total) VALUES (%s, %s, %s, %s, %s, %s)", (username, date, gallon, address, suggested_price, total_price))
   mysql.connection.commit()