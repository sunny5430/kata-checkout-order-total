class Order:

    def __init__(self):
        self.itemPrice = {}
        self.itemUnit = {}
        self.basket = {}
    
    def create_item(self, itemname, unit_type, unit_price):
        self.itemPrice[itemname] = unit_price
        self.itemUnit[itemname] = unit_type
    
    def scan(self, itemname, weight=0):
        if itemname not in self.itemPrice:
            raise KeyError("Item not exists.")

        if itemname in self.basket:
            if self.itemUnit[itemname] == "unit":
                self.basket[itemname] += 1
            else:
                self.basket[itemname] += weight
        else:
            if self.itemUnit[itemname] == "unit":
                self.basket[itemname] = 1
            else:
                self.basket[itemname] = weight
        
        print(self.basket)
    
    def cal_total(self):
        total = 0
        for item, quantity in self.basket.items():
            print(item, quantity)
            total += self.itemPrice[item] * quantity
        
        return total
    
