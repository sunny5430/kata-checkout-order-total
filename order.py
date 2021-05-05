class Item:
    def __init__(self, itemname, unit_type, unit_price):
        self.itemname = itemname
        self.unit_type = unit_type
        self.unit_price = unit_price

class Order:
    def __init__(self):
        self.itemList = {}
        self.basket = {}
        self.markdown = {}
    
    def create_item(self, itemname, unit_type, unit_price):
        item = Item(itemname, unit_type, unit_price)
        self.itemList[itemname] = item
        # self.itemPrice[itemname] = unit_price
        # self.itemUnit[itemname] = unit_type
    
    def scan(self, itemname, weight=0):
        if itemname not in self.itemList:
            raise KeyError("Item not exists.")
        
        item = self.itemList[itemname]

        if itemname in self.basket:
            if item.unit_type == "unit":
                self.basket[itemname] += 1
            else:
                self.basket[itemname] += weight
        else:
            if item.unit_type == "unit":
                self.basket[itemname] = 1
            else:
                self.basket[itemname] = weight
        

    def cal_total(self):
        total = 0
        for itemname, quantity in self.basket.items():
            item = self.itemList[itemname]
            if itemname in self.markdown:
                finalPrice = item.unit_price - self.markdown[itemname]
            else:
                finalPrice = item.unit_price
            
            # print(f"add {itemname}, {finalPrice}, {quantity}")
            total += finalPrice * quantity
        
        return total
    
    def remove(self, itemname, quantity):
        if itemname not in self.itemList or itemname not in self.basket:
            raise KeyError("Item not exists.")

        item = self.itemList[itemname]
        if item.unit_type == "unit" and type(quantity) != int:
            raise ValueError("Item should be remove on UNIT basis.")

        if self.basket[itemname] >= quantity:
            self.basket[itemname] -= quantity
        else:
            raise ValueError("Not enough quantity to remove.")

        print(self.basket)

    def create_markdown(self, itemname, priceoff):
        if priceoff < 0:
            raise ValueError("Priceoff should be greater than 0")

        item = self.itemList[itemname]
        if priceoff > item.unit_price:
            raise ValueError("Priceoff greater than original price.")
        
        self.markdown[itemname] = priceoff
            

