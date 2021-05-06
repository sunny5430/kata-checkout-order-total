from item import Item

class Order:
    def __init__(self):
        self.itemList = {}
        self.basket = {}
        self.markdown = {}
        self.specials = {}
    
    def create_item(self, itemname, unitType, unitPrice):
        item = Item(itemname, unitType, unitPrice)
        self.itemList[itemname] = item
    
    def scan(self, itemname, weight=None):
        if itemname not in self.itemList:
            raise KeyError("Item not exists.")
       
        item = self.itemList[itemname]
        if item.unit_type == "unit" and weight:
            raise ValueError("This item is counted in units.")
        if item.unit_type == "weight" and (not weight or weight <= 0):
            raise ValueError("Weight should be greater than 0.")

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
    
    def remove(self, itemname, quantity):
        if itemname not in self.basket:
            raise KeyError("Item not exists.")
        
        if quantity <= 0:
            raise ValueError("Quantity should be greater than 0.")

        item = self.itemList[itemname]
        if item.unit_type == "unit" and type(quantity) != int:
            raise ValueError("Item should be remove on UNIT basis (integer).")

        if self.basket[itemname] < quantity:
            raise ValueError("Not enough quantity to remove.")
        
        self.basket[itemname] -= quantity
        

    def cal_total(self):
        total = 0
        for itemname, quantity in self.basket.items():
            item = self.itemList[itemname]
            finalPrice = item.unit_price
            
            if itemname in self.markdown:
                finalPrice = item.unit_price - self.markdown[itemname]

            if itemname in self.specials:
                if self.specials[itemname]["type"] == "BuyAndGet":
                    total += self.cal_total_with_special_buyMgetN(itemname, quantity, finalPrice)
                elif self.specials[itemname]["type"] == "bundle":
                    total += self.cal_total_with_special_bundle(itemname, quantity, finalPrice)
            else:
                total += finalPrice * quantity
        
        return total
    
    def cal_total_with_special_buyMgetN(self, itemname, quantity, finalPrice):
        condition = self.specials[itemname]["condition"]
        discount_rate = self.specials[itemname]["discount_rate"]
        limit = self.specials[itemname]["limit"]
        total = 0
        if quantity < condition:
            total += finalPrice * quantity
            return total

        if not limit or quantity < limit:
            remaining = quantity % condition
            discount_quantity = quantity - remaining
        else:
            remaining = quantity - limit
            discount_quantity = limit
        
        total += remaining * finalPrice
        total += discount_quantity * finalPrice * (1- discount_rate)

        return total

    def cal_total_with_special_bundle(self, itemname, quantity, finalPrice):
        bundleCnt = self.specials[itemname]["bundleCnt"]
        bundlePrice = self.specials[itemname]["bundlePrice"]
        limit = self.specials[itemname]["limit"]
        total = 0

        if quantity < bundleCnt:
            total += finalPrice * quantity
            return total

        if not limit or quantity < limit:
            remaining = quantity % bundleCnt
            numBundle = (quantity - remaining) // bundleCnt
        else: 
            remaining = quantity - limit
            numBundle = limit // bundleCnt
        
        total += remaining * finalPrice
        total += numBundle * bundlePrice
        
        total = min(total, finalPrice * quantity)
        return total
    
    def create_markdown(self, itemname, priceoff):
        if itemname not in self.itemList:
            raise KeyError("Item not exists.")
        
        if priceoff < 0:
            raise ValueError("Priceoff should be greater than 0")

        item = self.itemList[itemname]
        if priceoff > item.unit_price:
            raise ValueError("Priceoff greater than original price.")
        
        self.markdown[itemname] = priceoff
            

    def create_special(self, itemname, buyM, getN, limit=None, priceoff=1):
        """
        suppose unit price = $10
        Buy 1 get 1 free: 
            buy 1, pay $10
            buy 2, pay $10 (special applied)
            buy 3, pay $20
            buy 4, pay $20 (special applied)

        Buy 2 get 1 free:
            buy 1, pay $10
            buy 2, pay $20
            buy 3, pay $20 (special applied)
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
        
        if itemname in self.specials:
            raise KeyError("Duplicate specials on same item")
        
        if buyM < getN:
            raise ValueError("Number of bought items should be greater than numbers of ites given for free.")

        if priceoff < 1:
            condition = buyM
            discount_rate = priceoff * getN / buyM
        else:
            condition = buyM + getN
            discount_rate = getN / (buyM + getN)

        self.specials[itemname] = {
            "type": "BuyAndGet",
            "condition": condition,
            "discount_rate": discount_rate,
            "limit": limit
        }


    def create_special_bundle(self, itemname, bundleCnt, bundlePrice, limit=None):
        if itemname not in self.itemList:
            raise KeyError("Item not exists.")
        
        if itemname in self.specials:
            raise KeyError("Duplicate specials on same item")
        
        self.specials[itemname] = {
            "type": "bundle",
            "bundleCnt": bundleCnt,
            "bundlePrice": bundlePrice,
            "limit": limit
        }
