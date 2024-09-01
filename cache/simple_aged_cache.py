from datetime import datetime, timedelta

class SimpleAgedCache:
    """
    Initializes a SimpleAgedCache priority queue.
    
    Parameters: clock=datetime.utcnow
    clock is a function which when called returns current time as a datetime object.
    """
    def __init__(self, clock=datetime.utcnow):
        self.clock = clock
        self.head: SimpleAgedCache.ExpirableEntry = None
        self.length: int = 0


    """
    Inserts a key-value pair into the SimpleAgedCache object.

    Parameters: key, value, retention_in_millis.
    retention_in_millis is the time the object is retained before cleaned up.
    """
    def put(self, 
            key, value, 
            retention_in_millis: int):
        self.clean_expired()
        
        new_elem: SimpleAgedCache.ExpirableEntry = self.create_entry(key, value, retention_in_millis)
        curr_elem: SimpleAgedCache.ExpirableEntry = self.head
        prev_elem: SimpleAgedCache.ExpirableEntry = None
        
        while curr_elem != None and new_elem.time_to_live() > curr_elem.time_to_live():
            prev_elem, curr_elem = curr_elem, curr_elem.next
        
        new_elem.next = curr_elem
        if prev_elem == None:
            self.head = new_elem
        else:
            prev_elem.next = new_elem
        self.length += 1

    """
    Returns True or False according to if the SimpleAgedCache object is empty.
    """
    def is_empty(self):
        return self.size() == 0

    """
    Returns the size of SimpleAgedCache.
    Removes expired elements.
    """
    def size(self):
        self.clean_expired()
        return self.length

    """
    Removes expired ExpirableEntry objects from SimpleAgedCache priority queue.
    """
    def clean_expired(self):
        while self.head != None and self.head.is_expired():
            self.head = self.head.next
            self.length -= 1

    """
    Returns the value for the given key.
    If there is no object with given key, returns None.
    Removes expired elements.

    Parameters: key.
    """
    def get(self, key):
        self.clean_expired()
        elem = self.head
        while elem != None:
            if elem.key == key:
                return elem.value
            elem = elem.next

        return None

    """
    Factory method for creating new ExpirableEntry objects.

    Parameters: key, value, retention_in_millis.
    retention_in_millis is the time the object is retained before cleaned up.
    """
    def create_entry(self, 
                     key, value, 
                     retention_in_millis):
        return SimpleAgedCache.ExpirableEntry(key, value, 
                                              self.clock() + timedelta(milliseconds=retention_in_millis), 
                                              self.clock)
    
    """
    ExpirableEntry inner class for entries that expire after a set amount of time.
    """
    class ExpirableEntry:
        """
        Initializes an ExpirableEntry object.

        Parameters: value, expiration_time, clock
        expiration_time is the time in milliseconds when the object should be cleaned up.
        clock is a function which when called returns current time as a datetime object.
        """
        def __init__(self, 
                     key, value, 
                     expiration_time, 
                     clock):
            self.key = key
            self.value = value
            self.time_to_live = lambda: (expiration_time - clock())
            self.next: SimpleAgedCache.ExpirableEntry = None

        """
        Returns True or False according to if the ExpriableEntry object is expired.
        """
        def is_expired(self):
            return self.time_to_live() <= timedelta(0)