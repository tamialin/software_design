class FuelPricing:
   def __init__(self,current_price, company_profit):
      self.__current_price = 1.5
      self.__company_profit = 0.1
      self.__gallon_factor
      self.__location_factor
      self.__history

   def calculatingPrice(self, gallon, state):
      return_customer = False

      if gallon > 1000:
         self.__gallon_factor = 0.02
      else:
         self.__gallon_factor = 0.03

      if state == "TX":
         self.__location_factor = 0.02
      else:
         self.__location_factor = 0.04
         
      if return_customer == "False":
         self.__history = 0.01
      else:
         self.__history = 0.0
      
      margin = self.__location_factor - self.__history + self.__gallon_factor - self.__company_profit
      suggested_price =  margin * self.current_price

      total_amount = gallon * suggested_price

      return suggested_price, total_amount

      