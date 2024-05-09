from Services.DataValidator import DataValidator
from Exceptions.NoMatchingItemException import NoMatchingItemException

class RatingsCollection():
    def __init__(self, dataValidator: DataValidator) -> None:
        self._collection = []
        self._dataValidator = dataValidator
        
    def getRatingById(self, id: str) -> dict:
        print(f"Inside 'getRatingsById' (function of RatingsCollection) with id: {id}")
        for rating in self._collection:
            if rating["id"] == id:
                return rating
        raise NoMatchingItemException(f"There is no book with the given id: {id}")
    
    def getTopRatedBooks(self) -> list:
        print("Inside 'getTopRatedBooks' (function of RatingsCollection)")
        topRatedBooks = []
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
    
    
    def createNewRating(self, data: dict, initialValues: list = None) -> None:
        print(f"Inside 'createNewRating' (function of RatingsCollection) with data: {data}.\ninitialValues is: {initialValues}")
        self._dataValidator.validateDataForCreateNewRating(data)
        values = initialValues if initialValues is not None else []
        average = 0 
        if initialValues is not None and initialValues != []:
            print(f'initialValues is: {initialValues}')
            average = round((sum(initialValues) / len(initialValues)), 2)
        self._collection.append({"id": data["id"], "title": data["title"], "values": values, "average": average})
        

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
        
    
    def __getListOfObjectsContainingOnlyIdTitleAverage(self, listForProcessing) -> list:
        return list(map(lambda item: {"id": item["id"], "title": item["title"], "average": item["average"]}, listForProcessing))
    
