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
      suggested_price =  round(margin * self.__current_price, 2)
      total_price = round(float(gallon * suggested_price), 2)

      return suggested_price, total_price