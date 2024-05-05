from Services.DataValidator import DataValidator
from Exceptions.NoMatchingItemException import NoMatchingItemException

class RatingsCollection():
    # TODO: Make sure float has only 2 digits after floating point
    def __init__(self, dataValidator: DataValidator) -> None:
        self._collection = []
        self._dataValidator = dataValidator
        
    def getRatingById(self, id: str) -> dict:
        # TODO: Should return all the json/without the values: []?
        print(f"Inside 'getRatingsById' (function of RatingsCollection) with id: {id}")
        for rating in self._collection:
            if rating["id"] == id:
                return rating
        raise NoMatchingItemException(f"There is no book with the given id: {id}")
        # TODO: Is it ok to return dict instead of a json? I think it will become a json in the api call
    
    # TODO: Questions from the paper on the table
    # TODO: Questions from forum
    # TODO: Check why I have to save another array with the top scores? It's unnecessary duplication...
    def getTopRatedBooks(self) -> list:
        print("Inside 'getTopRatedBooks' (function of RatingsCollection)")
        topRatedBooks = []
        # TODO: Check if 100 is good
        lastRatingAverage = 100
        ratingsWith3RatingsOrMore = list(filter(lambda rating: len(rating["values"]) >= 3, self._collection))
        sortedRatingsCollectionWith3RatingsOrMore = sorted(ratingsWith3RatingsOrMore, key=lambda rating: rating["average"])
        for rating in reversed(sortedRatingsCollectionWith3RatingsOrMore):
            if len(topRatedBooks) >= 3 and rating["average"] != lastRatingAverage:
                return self.__getListOfObjectsContainingOnlyIdTitleAverage(topRatedBooks)
            else:
                topRatedBooks.append(rating)
                lastRatingAverage = rating["average"]
        return self.__getListOfObjectsContainingOnlyIdTitleAverage(topRatedBooks)
    
    
    def createNewRating(self, data: dict) -> None:
        print(f"Inside 'createNewRating' (function of RatingsCollection) with data: {data}")
        self._dataValidator.validateDataForCreateNewRating(data)
        self._collection.append({"id": data["id"], "title": data["title"], "values": [], "average": 0})

    def deleteRating(self, id: str) -> None:
        print(f"Inside 'deleteRating' (function of RatingsCollection) with id: {id}")
        originalCollectionLength = len(self._collection)
        self._collection = [document for document in self._collection if document["id"] != id]
        if len(self._collection) == originalCollectionLength:
            raise NoMatchingItemException(f"The id which was asked to be deleted ({id}) doesn't exist")
        
    def addRatingValueToBookAndReturnNewAverage(self, id: str, value: int) -> float:
        print(f"Inside 'addRatingValueToBookAndReturnNewAverage' (function of RatingsCollection) with id: {id} and value: {value}")
        rating = self.getRatingById(id)
        print(rating["values"])
        rating["values"].append(value)
        rating["average"] = round(sum(rating["values"]) / len(rating["values"]), 2)
        return rating["average"]
    
    def doRatingWithGivenIdAlreadyExist(self, id: str) -> bool:
        print(f"Inside 'doRatingWithGivenIdAlreadyExist' (function of RatingsCollection) with id: {id}")
        try:
            rating = self.getRatingById(id)
            return True
        except NoMatchingItemException:
            return False
        # TODO: What id there another exception
        
    
    def __getListOfObjectsContainingOnlyIdTitleAverage(self, listForProcessing) -> list:
        return list(map(lambda item: {"id": item["id"], "title": item["title"], "average": item["average"]}, listForProcessing))