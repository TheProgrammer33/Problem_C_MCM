class Wallet:

    def __init__(self) -> None:
        self.wallet = {"USD": 1000, "Gold": 0, "BTC": 0}
    
    def buyBTC(self, price):
        self.wallet["USD"] -= price
        self.wallet["BTC"] += price

    def sellBTC(self, price):
        self.wallet["USD"] += price
        self.wallet["BTC"] -= price

    def buyGold(self, price):
        self.wallet["USD"] -= price
        self.wallet["Gold"] += price

    def sellGold(self, price):
        self.wallet["USD"] += price
        self.wallet["Gold"] -= price