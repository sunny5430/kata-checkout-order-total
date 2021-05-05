class Order:

    def __init__(self):
        self.itemPrice = {}
        self.itemUnit = {}
        self.basket = {}
        self.markdown = {}
    
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
        

    def cal_total(self):
        total = 0
        for item, quantity in self.basket.items():
            print(item, quantity)
            if item in self.markdown:
                finalPrice = self.itemPrice[item] - self.markdown[item]
            else:
                finalPrice = self.itemPrice[item]
                
            total += finalPrice * quantity
        
        return total
    
    def remove(self, itemname, quantity):
        if itemname not in self.itemPrice or itemname not in self.basket:
            raise KeyError("Item not exists.")
        
        if self.itemUnit[itemname] == "unit" and type(quantity) != int:
            raise ValueError("Item should be remove on UNIT basis.")

        if self.basket[itemname] >= quantity:
            self.basket[itemname] -= quantity
        else:
            raise ValueError("Not enough quantity to remove.")

        print(self.basket)

    def create_markdown(self, itemname, priceoff):
        if priceoff < 0:
            raise ValueError("Priceoff should be greater than 0")

        if priceoff > self.itemPrice[itemname]:
            raise ValueError("Priceoff greater than original price.")
        self.markdown[itemname] = priceoff
            

