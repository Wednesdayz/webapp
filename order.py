from Item import Item, food, meal, drinks
from abc import ABC, abstractmethod 

class Orders():
    def __init__(self, ID):
        self._total_price = 0
        self._pick_up_location = ""
        self._status = "Ordering"
        self._ID = ID
        self._items_ordered = []

    def add_to_order(self, meal):
        self._items_ordered.append(meal)
       
    def calculate_price(self):
        totalPrice = 0
        for item in self._items_ordered:
            totalPrice += item.price
                
        return totalPrice
    
    def tabulate_order(self):
        totalPrice = 0
        order_items = []
        for items in self._items_ordered:
            totalPrice = totalPrice + items.price
            cost = items.price
            order_items.append(items, "$" + str(cost))
    
        table = {
            'items': order_items,
            'total': totalPrice
        }
        self._price = totalPrice
        return table
        
    
    
    def add_item(self, meal):
        self._items_ordered.append(meal)
        
    def clear_order(self):
        self._items_ordered = []
        self._status = "Ordering"
        self._price = 0
    
    #getters and setters
    @property
    def ID(self):
        return self._ID
        
    @ID.setter
    def ID(self, ID):
        self._ID = ID
        
    @property
    def items_ordered(self):
        return self._items_ordered
        
    @property
    def status(self):
        return self._status
        
    @status.setter
    def status(self, newStatus):
        self._status = newStatus
    
    @property
    def price(self):
        return self._price
        
    @property
    def pick_up_location(self):
        return self._pick_up_location

    @pick_up_location.setter
    def pick_up_location(self, newLocation):
        self._pickup = newLocation

class PiggyBackOrder():
    def __init__(self, ID):
        self._total_price = 0
        self._pick_up_location = ""
        self._status = "Ordering"
        self._ID = ID
        self._list_of_orders = []

    def calculate_price(self):
        totalPrice = 0
        for items in self._list_of_orders:
            for items_ordered in items:
                totalPrice += items_ordered.price
                
        return totalPrice
    
    def tabulate_order(self):
        totalPrice = 0
        order_details = []
        order_items = []
        list_of_order_prices = []
        

        for items in self._list_of_orders:
            order_details.append(items.name)

            for items_ordered in items:
                totalPrice = totalPrice + items_ordered.price
                cost = items_ordered.price
                order_items.append(items, "$" + str(cost))
            
            table = {
                'Name' : order_details,
                'items': order_items,
                'total': totalPrice
            }
            list_of_order_prices.append(totalPrice)            
            order_items = []
            list_of_order_prices = []
            
        return table

        
    def clear_order(self):
        self._items_ordered = []
        self._status = "Ordering"
        self._price = 0
    
    #getters and setters
    @property
    def ID(self):
        return self._ID
        
    @ID.setter
    def ID(self, ID):
        self._ID = ID
        
    @property
    def items_ordered(self):
        return self._items_ordered
        
    @property
    def status(self):
        return self._status
        
    @status.setter
    def status(self, newStatus):
        self._status = newStatus
    
    @property
    def price(self):
        return self._price
        
    @property
    def pick_up_location(self):
        return self._pick_up_location

    @pick_up_location.setter
    def pick_up_location(self, newLocation):
        self._pickup = newLocation
