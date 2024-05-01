from Services.DataValidator import DataValidator
from Exceptions.NoMatchingItemException import NoMatchingItemException

class RatingsCollection():
    # TODO: Make sure float has only 2 digits after floating point
    def __init__(self, dataValidator: DataValidator) -> None:
        self._collection = []
        self._dataValidator = dataValidator
        
    def getRatingById(self, id: str) -> dict:
        for rating in self._collection:
            if rating["id"] == id:
                return rating
        raise NoMatchingItemException(f"There is no book with the given id: {id}")
        # TODO: Is it ok to return dict instead of a json? I think it will become a json in the api call
    
    # TODO: Check why I have to save another array with the top scores? It's unnecessary duplication...
    def getTopRatedBooks(self) -> list:
        # TODO: Implement
        return []
    
    def createNewRating(self, data: dict) -> None:
        self._dataValidator.validateDataForCreateNewRating(data)
        self._collection.append({"id": data["id"], "title": data["title"], "values": [], "average": 0})
    
    def deleteRating(self) -> None:
        # TODO: Implement
        return
        
    def addRatingValueToBookAndReturnNewAverage(self, id: str, value: int) -> float:
        # TODO: Implement
        return
    
    def doRatingWithGivenIdAlreadyExist(self, id: str) -> bool:
        try:
            rating = self.getRatingById(id)
            return True
        except NoMatchingItemException:
            return False
        # TODO: What id there another exception
    