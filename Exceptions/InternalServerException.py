class InternalServerException(Exception):
    
    def __init__(self, message="Unknown"):
        self.message = message
        super().__init__(self.message)