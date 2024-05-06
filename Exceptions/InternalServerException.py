class InternalServerException(Exception):
    
    def __init__(self, message="Unknown") -> None:
        self.message = message
        super().__init__(self.message)