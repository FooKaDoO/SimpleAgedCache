from datetime import datetime, timedelta, timezone

class SimpleAgedCache:
    """
    ExpirableEntry inner class for entries that expire after a set amount of time.
    """
    class ExpirableEntry:
        """
        Initializes an ExpirableEntry object.

        Parameters: value, expiration_time, clock
        expiration_time is a datetime object of when the object should be cleaned up.
        """
        def __init__(self, 
                     key, value, 
                     expiration_time: datetime):
            self.key = key
            self.value = value
            self.expiration_time: datetime = expiration_time
            self.next = None

        """
        Returns True or False according to if the ExpriableEntry object is expired.
        
        Parameters: curr_time.
        curr_time is current time as a datetime object.
        """
        def is_expired(self, curr_time: datetime):
            return self.expiration_time <= curr_time

    """
    Decorator for removing expired ExpirableEntry objects from SimpleAgedCache priority queue.
    """
    def clean_expired(function):
        def wrapper(*args, **kwargs):
            cache = args[0] # args[0] is the SimpleAgedCache object passed as self in a function parameter
            while cache.head != None and cache.head.is_expired(cache.clock()):
                cache.head = cache.head.next
                cache.length -= 1
            return function(*args, **kwargs)
        return wrapper

    """
    Initializes a SimpleAgedCache priority queue.

    Parameters: clock=datetime.utcnow
    clock is a function which when called returns current time as a datetime object.
    """
    def __init__(self, clock = lambda: datetime.now(timezone.utc)):
        self.clock = clock
        self.head: self.ExpirableEntry = None
        self.length: int = 0

    """
    Inserts a key-value pair into the SimpleAgedCache object.

    Parameters: key, value, retention_in_millis.
    retention_in_millis is the time the object is retained before cleaned up.
    """
    @clean_expired
    def put(self, 
            key, value, 
            retention_in_millis: int):
        new_elem: self.ExpirableEntry = self.ExpirableEntry(key, value, self.clock() + timedelta(milliseconds=retention_in_millis))
        curr_elem: self.ExpirableEntry = self.head
        prev_elem: self.ExpirableEntry = None
        
        while curr_elem != None and new_elem.expiration_time > curr_elem.expiration_time:
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
    @clean_expired
    def is_empty(self):
        return self.head is None

    """
    Returns the size of SimpleAgedCache.
    """
    @clean_expired
    def size(self):
        return self.length

    """
    Returns the value for the given key.
    If there is no object with given key, returns None.

    Parameters: key.
    """
    @clean_expired
    def get(self, key):
        elem = self.head
        while elem != None:
            if elem.key == key:
                return elem.value
            elem = elem.next
        return None