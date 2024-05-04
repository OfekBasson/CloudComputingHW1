from Services.ApiInvoker import ApiInvoker
# TODO: What is Provide and inject for?
from dependency_injector.wiring import Provide, inject
from Exceptions.NoMatchingItemsInApiGetCallException import NoMatchingItemsInApiGetCallException
from Exceptions.EmptyCollectionException import EmptyCollectionException
from Exceptions.NoMatchingItemException import NoMatchingItemException
from Exceptions.InvalidRequestBodyException import InvalidRequestBodyException
from Services.DataProcessor import DataProcessor
from Models.RatingsCollection import RatingsCollection

class BooksCollection():
    # TODO: Do the order matter?
    # TODO: Is this a good practice to return None from constructor?
    def __init__(self, dataProcessor: DataProcessor, ratingsCollection: RatingsCollection) -> None:
        # TODO: Add reference to numberOfOperations in every operation?
        # TODO: What is the _numberOfOperationsSoFar for?
        self._numberOfOperationsSoFar = 0
        self._collection = []
        # TODO: should I add underscore before variable name?
        self._dataProcessor = dataProcessor
        self._ratingsCollection = ratingsCollection
        
    # TODO: Change to "retreiveDataAndInsert..."" and split the retrieving and the insertion
    def insertBookAndReturnId(self, requestBody: dict) -> str:
        # TODO: Add logic here
        print(f"Inside 'insertBookAndReturnId' (function of 'BooksCollection). requestBody is: {requestBody}")
        try:
            self._numberOfOperationsSoFar += 1
            fullBookData = self._dataProcessor.constructFullBookData(requestBody)
            self._collection.append(fullBookData)
            self._ratingsCollection.createNewRating(fullBookData)
            id = fullBookData["id"]
            return id
            # return ""
        # TODO: print error message?
        except NoMatchingItemsInApiGetCallException as exception:
            return requestBody
        
    
    def getCollectionFilteredByQuery(self, query: dict) -> list:
        print(f"Inside 'getCollectionFilteredByQuery' (function of 'BooksCollection'). with query: {query}")
        print(query.items())
        # TODO: Is numOps relevant?
        self._numberOfOperationsSoFar += 1
        if len(self._collection) == 0:
            raise EmptyCollectionException("The collection is empty")
        
        collectionCopy = self._collection.copy()
        print(f'collectionCopy is: {collectionCopy}')
        for queryKey, queryValue in query.items():
            if queryValue is not None:
                print(f"Filtering now by '{queryKey}': '{queryValue}'")
                collectionCopy = list(filter(lambda document: self.__isQueryParameterSatisfiedByDocument(document, queryKey, queryValue), collectionCopy))
                print(f"Finished filtering for '{queryKey}': '{queryValue}'. There are {len(collectionCopy)} books which matches the criteria so far")
        if len(collectionCopy) == 0:
            raise EmptyCollectionException("There are no books matching your criteria")
        
        return collectionCopy
    
    def getBookById(self, id: str) -> dict:
        print(f"Entered 'getBookById' (function of 'BooksCollection') with id: {id}")
        try:
            book = self.getCollectionFilteredByQuery({"id": id})[0]
            return book
        except EmptyCollectionException as exception:
            raise NoMatchingItemException("There is no matching book to the provided id")
        
    def doBookWithGivenIsbnAlreadyExist(self, isbn: str) -> bool:
        print(f"Inside 'doBookWithGivenIsbnAlreadyExist' (function of 'BooksCollection') with ISBN: {isbn}")
        try:
            book = self.getCollectionFilteredByQuery({"ISBN": isbn})[0]
            return True
        except (NoMatchingItemException, EmptyCollectionException) as exception:
            return False
        
    def deleteBookById(self, id: str) -> str:
        print(f"Inside 'deleteBookById' (function of 'BooksCollection') with id: {id}")
        # TODO: If it doesn't exist in the collection - should I return the same collection?
        originalCollectionLength = len(self._collection)
        self._collection = [document for document in self._collection if document["id"] != id]
        if len(self._collection) == originalCollectionLength:
            raise NoMatchingItemException("The id which was asked to be deleted doesn't exist")
        self._ratingsCollection.deleteRating(id)
        return id
    
    # TODO: Should do something with the ratings collection?
    def updateSpecificDocumentFromCollection(self, idOfDocumentToUpdate: str, requestBody: dict) -> str:
        try:
            print(f"Inside 'updateSpecificDocumentFromCollection' (function of 'BooksCollection') with idOfDocumentToUpdate: {idOfDocumentToUpdate} and requestBody: {requestBody}")
            updatedResourceId = requestBody["id"]
            # TODO: Doesn't it return the id of the deleted document? What if they are different from each other (also the new id)?
            self.deleteBookById(idOfDocumentToUpdate)
            self._collection.append(requestBody)
            return updatedResourceId
        
        except KeyError:
            raise InvalidRequestBodyException(f"The request body has no 'id' field. Request body is: {requestBody}")
            
                
    def __isQueryParameterSatisfiedByDocument(self, document: dict, queryKey: str, queryValue: str) -> bool:
        print(f"Inside '__isQueryParameterSatisfiedByDocument' (function of 'BooksCollection') with document: {document} and query: {queryKey}={queryValue}")
        # TODO: if there is a key error - need to handle it
        documentValue = document[queryKey]
        # TODO: It won't be language. How does if influence (I think authors is also a list)??? Slide 19 is not clear
        if type(documentValue) is list:
            return queryValue in documentValue
        return documentValue == queryValue
            
        
            
        
        
