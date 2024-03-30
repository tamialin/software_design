from flask import Flask, jsonify, request, redirect, url_for, render_template, session
from utils.pricing import FuelPricing
from utils.history import update_quote_history

def fuelQuote():
   if request.method == 'POST':
      gallon = float(request.form["gallonsRequested"]) # get amount of gallon from html file
      pricingModule = FuelPricing()
      suggested_price, total_price = pricingModule.calculatingPrice(gallon)

      # Assuming you have access to the username through session or some other means
      username = "user1"  # Replace with actual username retrieval logic

        # Prepare quote data
      quote_data = {
            'gallon': gallon,
            'suggested_price': suggested_price,
            'total_price': total_price
      }
        # Update quote history
      update_quote_history(username, quote_data)
      
      return jsonify(suggested_price = suggested_price, total_price = total_price)
   # send user input and prices to history backend
   return render_template('quote.html')  