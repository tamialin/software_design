class FuelPricing:
    def __init__(self):
        self.current_price = 1.5
        self.company_profit = 0.1
        self.location_factor = 0.04
        self.history_factor = 0.01
        self.__history = None

    def calculatingPrice(self, gallon, return_customer=False):
        gallon_factor = 0.03 if gallon <= 1000 else 0.02

        if return_customer == False:  # Changed to compare with boolean False
            self.__history = 0.0
        else:
            self.__history = self.history_factor

        # Calculating the price
        margin = self.location_factor - self.__history + gallon_factor + self.company_profit
        suggested_price = round(margin * self.current_price, 2)
        total_price = round(float(gallon * suggested_price), 2)

        return suggested_price, total_price