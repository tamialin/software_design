from flask import Flask, jsonify, request, redirect, url_for, render_template, session
from utils.pricing import FuelPricing
from utils.history import update_quote_history
from utils.temp_db import users_db


def fuelQuote():
   if request.method == 'POST':
      gallon = float(request.form["gallonsRequested"])
      delivery_date = request.form["deliveryDate"] 
      pricingModule = FuelPricing()
      suggested_price, total_price = pricingModule.calculatingPrice(gallon)

      username = session.get("username") 

      # Prepare quote data
      if username:
         quote_data = {
            'delivery_date': delivery_date,
            'gallon_requested': gallon,
            'delivery_address': users_db[username]['address'],
            'suggested_price': suggested_price,
            'total_price': total_price,
               
         }
        # Update quote history
      update_quote_history(username, quote_data)
      
      return jsonify(suggested_price = suggested_price, total_price = total_price)
   # send user input and prices to history backend
   return render_template('quote.html')  