class InvalidRequestBodyException(Exception):
    
    def __init__(self, message="Request body is invalid") -> None:
        self.message = message
        super().__init__(self.message)