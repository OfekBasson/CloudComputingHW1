class NoMatchingItemsInApiGetCallException(Exception):
    
    def __init__(self, message="There isn't a book which matches the given ISBN in google books api") -> None:
        self.message = message
        super().__init__(self.message)