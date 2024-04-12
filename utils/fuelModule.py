from flask import Flask, jsonify, request, redirect, url_for, render_template, session
from utils.pricing import FuelPricing
from utils.history import update_quote_history
from utils.temp_db import users_db


def fuelQuote(mysql):
   if request.method == 'POST':

      # Get username from DB
      username = session.get("username")
      cur = mysql.connection.cursor()
      # cur.execute("SELECT * FROM users WHERE username = %s", (username,))
      # user = cur.fetchone()

      # Get address from profile
      cur.execute("SELECT address1, city, states from users WHERE username = %s", (username,))
      fetchValues = cur.fetchone()
      if fetchValues:
         address = fetchValues[0]
         city = fetchValues[1]
         state = fetchValues[2]
         deliveryAddress  = f"{address} - {city} - {state}"

      # Receive input from quote  page
      gallon = float(request.form["gallonsRequested"])
      date = request.form["deliveryDate"]
      pricingModule = FuelPricing()
      suggested_price, total_price = pricingModule.calculatingPrice(gallon, state)

      # address = request.form["deliveryAddress"]

         # # Prepare quote data
         # if username:
         #    quote_data = {
         #       'delivery_date': delivery_date,
         #       'gallon_requested': gallon,
         #       'delivery_address': users_db[username]['address1'],
         #       'suggested_price': suggested_price,
         #       'total_price': total_price,
         #    }
         # # Update quote history
         # update_quote_history(username, quote_data)

         # Return the value to display quote
      if 'displayData' in request.form:
         return jsonify(suggested_price = suggested_price, total_price = total_price)
      elif 'sendData' in request.form:
         sendToDB(mysql, username, date, gallon, address, suggested_price, total_price)
         return jsonify(success = True)

   # send user input and prices to history backend
   return render_template('quote.html')  

def sendToDB(mysql, username, date, gallon, address, suggested_price, total_price):
   username = session.get("username")
   cur = mysql.connection.cursor()
   cur.execute("SELECT * FROM users WHERE username = %s", (username,))
   user = cur.fetchone()

   cur.execute("INSERT INTO quote_history (username, date, gallon, address, price, total) VALUES (%s, %s, %s, %s, %s, %s)", (username, date, gallon, address, suggested_price, total_price))
   mysql.connection.commit()
   cur.close()