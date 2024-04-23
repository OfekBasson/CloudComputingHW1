import uuid

class BooksCollection():
    # TODO: Is this a good practice to return None from constructor?
    def __init__(self) -> None:
        self.numberOfOperationsSoFar = 0
        self.collection = {}
        
    def insertBookAndReturnId(self, title: str, ISBN: str, genre: str) -> str:
        # TODO: Add logic here
        self.numberOfOperationsSoFar += 1
        id = str(uuid.uuid4())
        return id
        
    