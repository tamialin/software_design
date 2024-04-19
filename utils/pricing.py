

class FuelPricing:
    def __init__(self):
        self.current_price = 1.5
        self.company_profit = 0.1
        self.location_factor = None
        self.history_factor = None

    def calculatingPrice(self, gallon, state, returnUser):
        gallon_factor = 0.03 if gallon <= 1000 else 0.02

        if returnUser == 0:  # Changed to compare with boolean False
            self.history_factor = 0.0
        else:
            self.history_factor = 0.01

        if state == "TX":
            self.location_factor = 0.02
        else:
            self.location_factor = 0.04

        # Calculating the price
        margin = round((self.location_factor - self.history_factor + gallon_factor + self.company_profit) * self.current_price, 3)
        suggested_price = round(margin + self.current_price, 3)
        total_price = round(float(gallon * suggested_price), 2)

        print(self.history_factor)

        return suggested_price, total_price