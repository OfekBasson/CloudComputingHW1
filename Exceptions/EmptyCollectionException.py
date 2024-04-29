class EmptyCollectionException(Exception):
    
    def __init__(self, message="Books collection is empty"):
        self.message = message
        super().__init__(self.message)