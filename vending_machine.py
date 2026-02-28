class VendingMachine():
    def __init__(self):
        self.items = {
             "Oreo": 2.50,
             "Chips": 1.75,
             "Cola": 1.50
        }

        self.balance = 0.0
    
    def insertmoney(self, amount):
               
            if amount > 0:
                self.balance += amount
                return f"Inserted €{amount:.2f}. Current balance: €{self.balance:.2f}"
            else:
                return "Please insert money"
            
    def purchase(self, item_name):
        
        if item_name not in self.items:
            return "Item not available."

        price = self.items[item_name]
        if self.balance >= price:
            self.balance -= price
            return f"Dispensing {item_name}. Remaining balance: €{self.balance:.2f}"
        else:
            return (
                f"Insufficient funds. {item_name} costs €{price:.2f}, "
                f"balance is €{self.balance:.2f}."
            )

    def refund(self):
        refunded = self.balance
        self.balance = 0.0
        return f"Refunding €{refunded:.2f}."        
        


