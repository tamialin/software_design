from flask import request, redirect, url_for, render_template
# from profileUpdate import states

class FuelPricing:
   def __init__(self):
      # Make all variables private
      self.__current_price = 1.5
      self.__company_profit = 0.1
      self.__gallon_factor = None

      # if states == "TX":
      #    self.__location_factor = 0.02
      # else:
      #    self.__location_factor = 0.04
      self.__location_factor = 0.04

      self.__history = None

   def calculatingPrice(self, gallon):
      return_customer = False

      if gallon > 1000:
         self.__gallon_factor = 0.02
      else:
         self.__gallon_factor = 0.03
         
      if return_customer == "False":
         self.__history = 0.0
      else:
         self.__history = 0.01
      
      #  Calculating the price
      margin = self.__location_factor - self.__history + self.__gallon_factor + self.__company_profit
      suggested_price =  margin * self.__current_price
      total_price = gallon * suggested_price

      return suggested_price, total_price

def fuelQuote():
   if request.method == 'POST':
      gallon = request.form['gallonsRequested']
      pricingModule = FuelPricing()
      suggested_price, total_price = pricingModule.calculatingPrice(gallon)
      return render_template('quote.html', 
                             suggested_price = suggested_price, 
                             total_price = total_price)
   return render_template('quote.html')