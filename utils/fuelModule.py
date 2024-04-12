from flask import Flask, jsonify, request, redirect, url_for, render_template, session
from utils.pricing import FuelPricing
from utils.history import update_quote_history
from utils.temp_db import users_db


def fuelQuote():
   if request.method == 'POST':
      username = session.get("username") 
      
      gallon = float(request.form["gallonsRequested"])
      delivery_date = request.form["deliveryDate"]
      pricingModule = FuelPricing()
      suggested_price, total_price = pricingModule.calculatingPrice(gallon)

      # If user hit the Get Quote Button
      if request.form.get('action') == 'get_quote':

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
         return jsonify(suggested_price = suggested_price, total_price = total_price)
      
      if 'submitBtn' in request.form:
         date = request.form["deliveryAddress"]

         cur = mysql.connection.cursor()
         cur.execute("INSERT INTO quote_history (username, date, gallon, address, price, total) VALUE (%s, %s, %f, %s, %s, %s, %s), (username, date, gallon, date, suggested_price, total_price)")
         
         mysql.connection.commit()
         cur.close()

   # send user input and prices to history backend
   return render_template('quote.html')  