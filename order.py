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
        self.specials = {}
    
    def create_item(self, itemname, unit_type, unit_price):
        item = Item(itemname, unit_type, unit_price)
        self.itemList[itemname] = item
    
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
            finalPrice = item.unit_price
            
            if itemname in self.markdown:
                finalPrice = item.unit_price - self.markdown[itemname]

            if itemname in self.specials:
                total += self.cal_total_with_special(itemname, quantity, finalPrice)
            else:
            
                # print(f"add {itemname}, {finalPrice}, {quantity}")
                total += finalPrice * quantity
        
        return total
    
    def cal_total_with_special(self, itemname, quantity, finalPrice):
        condition, discount_rate, limit = self.specials[itemname]
        total = 0

        if quantity < condition:
            total += finalPrice * quantity
            return total

        if not limit or quantity < limit:
            remaining = quantity % condition
            discount_quantity = quantity - remaining
        else: # quantity >= limit:
            remaining = quantity % limit
            discount_quantity = limit
        
        total += remaining * finalPrice
        total += discount_quantity * finalPrice * (1- discount_rate)

        print("cal price with special", itemname, condition, discount_rate, total)
        print("limit", limit)
        print(discount_quantity, finalPrice, (1- discount_rate))
        
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

        if itemname not in self.itemList:
            raise KeyError("Item not exists.")

        item = self.itemList[itemname]
        if priceoff > item.unit_price:
            raise ValueError("Priceoff greater than original price.")
        
        self.markdown[itemname] = priceoff
            

    def create_special(self, itemname, buyM, getN, limit=None, priceoff=1):
        """
        suppose unit price = $10
        Buy 1 get 1 free: 
            buy 1, pay $10
            buy 2, pay $10
            buy 3, pay $20
            buy 4, pay $20

        Buy 2 get 1 free:
            buy 1, pay $10
            buy 2, pay $20
            buy 3, pay $20
            buy 4, pay $30

        Buy 2 get 1 half off: 
            buy 1, pay $10
            buy 2, pay $15 (25% off/ each)
            buy 3, pay $25
            buy 4, pay $30 (25% off/ each)

        Buy 3 get 1 60% off:
            buy 1, pay $10
            buy 2, pay $20
            buy 3, pay $24 (20% off/ each)
            buy 4, pay $34

        """
        if itemname not in self.itemList:
            raise KeyError("Item not exists.")

        if priceoff < 1:
            condition = buyM
            discount_rate = priceoff / buyM

        else:
            condition = buyM + getN
            discount_rate = getN / (buyM + getN)

        self.specials[itemname] = [condition, discount_rate, limit]
