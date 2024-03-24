from flask import Flask, jsonify, request, redirect, url_for, render_template
from utils.pricing import FuelPricing

def fuelQuote():
   if request.method == 'POST':
      gallon = request.form["gallonsRequested"]
      pricingModule = FuelPricing()
      suggested_price, total_price = pricingModule.calculatingPrice(gallon)
      return render_template('quote.html', suggested_price = suggested_price, total_price = total_price)
   return render_template('quote.html')