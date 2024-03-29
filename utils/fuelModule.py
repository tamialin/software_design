from flask import Flask, jsonify, request, redirect, url_for, render_template, session
from utils.pricing import FuelPricing

def fuelQuote():
   if request.method == 'POST':
      gallon = float(request.form["gallonsRequested"]) # get amount of gallon from html file
      pricingModule = FuelPricing()
      suggested_price, total_price = pricingModule.calculatingPrice(gallon)
      return jsonify(suggested_price = suggested_price, total_price = total_price)
   return render_template('quote.html')