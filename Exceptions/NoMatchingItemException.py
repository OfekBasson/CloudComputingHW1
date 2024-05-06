class NoMatchingItemException(Exception):
    
    def __init__(self, message="No matching item in the collection") -> None:
        self.message = message
        super().__init__(self.message)