from abc import ABC, abstractmethod

class Item(ABC):
    def __init__(self, name, price, location, availability, ID, category):
        self._name = name
        self._price = price 
        self._location = location 
        self._availability = availability 
        self._ID = ID
        self._category = category

    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, item_name):
        self._name = item_name
    
    @property
    def price(self):
        return self._price

    @price.setter 
    def price(self, item_price):
        self._price = item_price

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, place):
        self._location = place
    
    @property
    def availability(self):
        return self._availability

    @availability.setter
    def availability(self, avail):
        self._availability = avail

    @property
    def ID(self):
        return self._ID
    
    @property
    def category(self):
        return self._category


class food(Item):
    def __init__(self, name, price, location, availability, ID, category, preparation_time):
        super().__init__(name, price, location, availability, ID, category)
        self._preparation_time = preparation_time
    
    
    @property
    def preparation_time(self):
        return self._preparation_time

    @preparation_time.setter
    def preparation_time(self, queue, average_wait, preparation_time):
        self._preparation_time = queue * average_wait + preparation_time 
    
    

class meal(Item):
    def __init__(self, name, price, location, availability, ID, preparation_time, category, part_of_meal):
        super().__init__(name, price, location, availability, ID, category)
        self._part_of_meal = []


    @property 
    def part_of_meal(self):
        return self._part_of_meal

    @part_of_meal.setter
    def part_of_meal(self, ingredients):
        for things in ingredients:
            self._part_of_meal.append(things)


class drinks(Item):
    def __init__(self, name, price, location, availability, ID, category, preparation_time):
        super().__init__(name, price, location, availability, ID, category)
        self._preparation_time = preparation_time
        
    @property
    def preparation_time(self):
        return self._preparation_time

    @preparation_time.setter
    def preparation_time(self, queue, average_wait, preparation_time):
        self._preparation_time = queue * average_wait + preparation_time 



        