from datetime import datetime, timedelta

class SimpleAgedCache:
    """
    Initializes a SimpleAgedCache object.
    Parameters: clock=datetime.utcnow
    clock is a function which when called returns the current time in milliseconds.
    """
    def __init__(self, clock=datetime.utcnow):
        self.clock = clock
        self.data: list = [None]
        self.length: int = 0
        self.capacity: int = 1

    """
    Adjust array size according to required elements.

    Parameters: required_capacity.
    required_capacity is an integer value of required extra
    capacity for adding new elements (can be negative if removing elements.)
    """
    def ensure_capacity(self, required_capacity: int):
        total_capacity = required_capacity + self.length
        if total_capacity > self.capacity:
            self.data = self.data + (total_capacity * 2 - self.capacity) * [None]
            self.capacity = total_capacity * 2
        elif total_capacity * 2 < self.capacity:
            self.data = self.data[:total_capacity + 1]
            self.capacity = total_capacity * 2


    """
    Inserts a key-value pair into the SimpleAgedCache object.

    Parameters: key, value, retention_in_millis.
    retention_in_millis is the time the object is retained before cleaned up.
    """
    def put(self, key, value, retention_in_millis: int):
        self.data[self.length] = self.create_entry(key, value, retention_in_millis)
        self.length += 1
        self.ensure_capacity(1)
    

    """
    Removes element at given index from SimpleAgedCache object.

    Parameters: index.
    index is the index at where the element is to be removed.
    """
    def remove(self, index: int):
        while index < self.length:
            self.data[index] = self.data[index + 1]
            index += 1
        self.length -= 1
        self.ensure_capacity(-1)

    """
    Returns True or False according to if the SimpleAgedCache object is empty.
    """
    def is_empty(self):
        return self.size() == 0

    """
    Returns the size of SimpleAgedCache.
    Removes expired elements and resizes data array.
    """
    def size(self):
        i = 0
        while i < self.length:
            elem = self.data[i]
            if elem.is_expired():
                self.remove(i)
            else:
                i += 1
        return self.length

    """
    Returns the element at the given key.
    If there is no object with given key, returns None.
    Removes expired elements and resizes data array.

    Parameters: key.
    """
    def get(self, key):
        i = 0
        while i < self.length:
            if self.data[i].key == key:
                if self.data[i].is_expired():
                    self.remove(i)
                    i -= 1
                else:
                    return self.data[i].value
            i += 1
        return None

    """
    Factory method for creating new ExpirableEntry objects.

    Parameters: value, retention_in_millis.
    retention_in_millis is the time the object is retained before cleaned up.
    """
    def create_entry(self, key, value, retention_in_millis):
        return SimpleAgedCache.ExpirableEntry(key, value, 
                                              self.clock() + timedelta(milliseconds=retention_in_millis), 
                                              self.clock)
    
    """
    ExpirableEntry inner class for entries that expire after a set amount of time.
    """
    class ExpirableEntry:
        """
        Initializes an ExpirableEntry object.

        Parameters: value, expiration_time, clock.
        expiration_time is the time in milliseconds when the object should be cleaned up.
        clock is a function which when called returns the current time in milliseconds.
        """
        def __init__(self, key, value, expiration_time, clock):
            self.key = key
            self.value = value
            self.expiration_time = expiration_time
            self.clock = clock
        
        """
        Returns True or False according to if the ExpriableEntry object is expired.
        """
        def is_expired(self):
            return self.clock() >= self.expiration_time