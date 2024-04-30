class InternalServerException(Exception):
    
    def __init__(self, message="Unable to connect to the service"):
        self.message = message
        super().__init__(self.message)