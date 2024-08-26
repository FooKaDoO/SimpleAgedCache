from datetime import datetime, timedelta

class SimpleAgedCache:
    """
    Initializes a SimpleAgedCache object.
    Parameters: clock=datetime.utcnow
    clock is a function which when called returns the current time in milliseconds.
    """
    def __init__(self, clock=datetime.utcnow):
        self.clock = clock
        self.entries = dict()

    """
    Inserts a key-value pair into the SimpleAgedCache object.

    Parameters: key, value, retention_in_millis.
    retention_in_millis is the time the object is retained before cleaned up.
    """
    def put(self, key, value, retention_in_millis: int):
        self.entries[key] = self.create_entry(value, retention_in_millis)

    """
    Returns True or False according to if the SimpleAgedCache object is empty.
    """
    def is_empty(self):
        return self.size() == 0

    """
    Returns the size of SimpleAgedCache.
    """
    def size(self):
        return len(self.entries)

    """
    Returns the element at the given key.
    If there is no object with given key, returns None.

    Parameters: key.
    """
    def get(self, key):
        item = self.entries.get(key)
        return None if item is None else item.value

    """
    Cleans up all expired entries from the SimpleAgedCache object.
    """
    def clean_expired_entries(self):
        to_clean_up = tuple(k for k, v in self.entries.items() if v.is_expired())
        for key in to_clean_up:
            del self.entries[key]

    """
    Overwritten __getattribute__ method so it calls clean_expired_entries()
    every time a method is called. 
    """
    def __getattribute__(self, name):
        attr = super().__getattribute__(name)
        if callable(attr):
            super().__getattribute__('clean_expired_entries')()
        return attr

    """
    Factory method for creating new ExpirableEntry objects.

    Parameters: value, retention_in_millis.
    retention_in_millis is the time the object is retained before cleaned up.
    """
    def create_entry(self, value, retention_in_millis):
        return SimpleAgedCache.ExpirableEntry(value, 
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
        def __init__(self, value, expiration_time, clock):
            self.value = value
            self.expiration_time = expiration_time
            self.clock = clock
        
        """
        Returns True or False according to if the ExpriableEntry object is expired.
        """
        def is_expired(self):
            return self.clock() >= self.expiration_time