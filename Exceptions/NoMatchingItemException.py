class NoMatchingItemException(Exception):
    
    def __init__(self, message="No matching item in the collection"):
        self.message = message
        super().__init__(self.message)