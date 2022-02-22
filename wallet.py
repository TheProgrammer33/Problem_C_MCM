class Wallet:

    def __init__(self) -> None:
        self.wallet = {"USD": 1000, "Gold": 0, "BTC": 0}
        self.fees = {"Gold": 0.01, "BTC": 0.02}
    
    def getAvailableMoney(self):
        return self.wallet["USD"]

    def getGoldAmount(self):
        return self.wallet["Gold"]

    def getBTCAmount(self):
        return self.wallet["BTC"]

    def getNetWorth(self, btcPrice, goldPrice):
        totalBTCMoney = self.wallet["BTC"] * btcPrice
        totalGoldMoney = self.wallet["Gold"] * goldPrice
        return (totalBTCMoney - (totalBTCMoney * self.fees["BTC"])) + (totalGoldMoney - (totalGoldMoney * self.fees["Gold"])) + self.wallet["USD"]

    def buy(self, product, price, numberOfProducts):
        # Spend money to buy product and add product to wallet
        self.wallet["USD"] -= round(price * numberOfProducts, 2)
        self.wallet[product] += numberOfProducts
        # Take away the fee
        self.wallet["USD"] -= round(price * numberOfProducts * self.fees[product], 2)

    def sell(self, product, price):
        numberOfProducts = self.wallet[product]
        # Receive money for selling product and remove product from wallet
        self.wallet["USD"] += round(price * numberOfProducts, 2)
        self.wallet[product] -= numberOfProducts
        # Take away the fee
        self.wallet["USD"] -= round(price * numberOfProducts * self.fees[product], 2)