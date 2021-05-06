from item import Item

class Order:
    def __init__(self):
        self.itemList = {}
        self.basket = {}
        self.markdown = {}
        self.specials = {}
    
    def create_item(self, itemname, unitType, unitPrice):
        """
        Create scannable items with name, type of unit, and price.
        """
        item = Item(itemname, unitType, unitPrice)
        self.itemList[itemname] = item
    
    def scan(self, itemname, weight=None):
        """
        Scan the item and add to basket.
        If the item's type of unit is 'unit', then no need to specify weight. 
        The count will increment by 1.
        """
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
        """
        Remove the item from the basket.
        Must specify the item's name and quantity to remove.
        """
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
        """
        Calculate and return the pre-tax total of current basket.
        Applied markdown and specials rules for items that applied to discounts.
        """
        total = 0
        for itemname, quantity in self.basket.items():
            item = self.itemList[itemname]
            finalPrice = item.unit_price
            
            if itemname in self.markdown:
                finalPrice = item.unit_price - self.markdown[itemname]

            if itemname in self.specials:
                if self.specials[itemname]["type"] == "BuyAndGet":
                    total += self.__cal_total_with_special_buyMgetN(itemname, quantity, finalPrice)
                elif self.specials[itemname]["type"] == "bundle":
                    total += self.__cal_total_with_special_bundle(itemname, quantity, finalPrice)
            else:
                total += finalPrice * quantity
        
        return total
    
    def __cal_total_with_special_buyMgetN(self, itemname, quantity, finalPrice):
        """
        Calculate and return pre-tax total for item applied to Buy M get N with X off discount.
        """
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

    def __cal_total_with_special_bundle(self, itemname, quantity, finalPrice):
        """
        Calculate and return pre-tax total for item applied to Buy M for $X discount.
        If both markdown and bundle sale are applied to the item,
        check and return the more favorable deal.
        """
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
        """
        Create a markdown deal on input item.
        """
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
        Create one of following types of special deal on input item.
        - Buy M get N for free (limit K)
        - Buy M get N X off (limit K)
        One item can only be applied with one special deal.
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
        """
        Create a 'Buy bundleCnt for $bundlePrice (limit K)' deal on input item.
        One item can only be applied with one special deal.
        """
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
