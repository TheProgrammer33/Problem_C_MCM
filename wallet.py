class Wallet:

    def __init__(self) -> None:
        self.wallet = {"USD": 1000, "Gold": 0, "BTC": 0}
        self.fees = {"Gold": 0.01, "BTC": 0.02}
    
    def getAvailableMoney(self):
        return self.wallet["USD"]

    def buy(self, product, price, numberOfProducts):
        self.wallet["USD"] -= round(price * numberOfProducts, 2)
        self.wallet[product] += numberOfProducts
        self.wallet["USD"] -= round(price * numberOfProducts * self.fees[product], 2)

    def sell(self, product, price):
        numberOfProducts = self.wallet[product]
        self.wallet["USD"] += round(price * numberOfProducts, 2)
        self.wallet[product] -= numberOfProducts
        self.wallet["USD"] -= round(price * numberOfProducts * self.fees[product], 2)