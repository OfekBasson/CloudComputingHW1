from Services.ApiInvoker import ApiInvoker
# TODO: What is Provide and inject for?
from dependency_injector.wiring import Provide, inject
from Exceptions.NoMatchingItemsInApiGetCallException import NoMatchingItemsInApiGetCallException
from Exceptions.EmptyCollectionException import EmptyCollectionException
from Exceptions.NoMatchingItemException import NoMatchingItemException
from Services.DataProcessor import DataProcessor
import asyncio

class BooksCollection():
    # TODO: Is this a good practice to return None from constructor?
    def __init__(self, dataProcessor: DataProcessor) -> None:
        # TODO: Add reference to numberOfOperations in eve1ry operation
        # TODO: What is the _numberOfOperationsSoFar for?
        self._numberOfOperationsSoFar = 0
        self._collection = []
        # TODO: should I add underscore before variable name?
        self._dataProcessor = dataProcessor
        
    # TODO: Change to "retreiveDataAndInsert..."" and split the retrieving and the insertion
    def insertBookAndReturnId(self, requestBody: dict) -> str:
        # TODO: Add logic here
        print(f"Inside 'insertBookAndReturnId' (function of 'BooksCollection). requestBody is: {requestBody}")
        try:
            self._numberOfOperationsSoFar += 1
            requestWithFullData = self._dataProcessor.constructFullBookData(requestBody)
            self._collection.append(requestWithFullData)
            id = requestWithFullData["id"]
            return id
            # return ""
        # TODO: print error message?
        except NoMatchingItemsInApiGetCallException as exception:
            return requestBody
        
    
    def getCollectionFilteredByQuery(self, query: dict) -> list:
        print(f"Inside 'getCollectionFilteredByQuery' (function of 'BooksCollection'). Query is: {query}")
        self._numberOfOperationsSoFar += 1
        if len(self._collection) == 0:
            raise EmptyCollectionException("The collection is empty")
        
        collectionCopy = self._collection.copy()
        for queryKey, queryValue in query.items():
            if queryValue is not None:
                print(f"Inside 'getCollectionFilteredByQuery' (function of 'BooksCollection'). Filtering now by '{queryKey}': '{queryValue}'")
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
        print(f"Entered 'doBookWithGivenIsbnAlreadyExist' (function of 'BooksCollection')")
        try:
            book = self.getCollectionFilteredByQuery({"ISBN": isbn})[0]
            return False
        except (NoMatchingItemException, EmptyCollectionException) as exception:
            return True
        
    def deleteBookById(self, id: str) -> str:
        # TODO: If it doesn't exist in the collection - should I return the same collection?
        originalCollectionLength = len(self._collection)
        self._collection = [document for document in self._collection if document["id"] != id]
        if len(self._collection) == originalCollectionLength:
            raise NoMatchingItemException("The id which was asked to be deleted doesn't exist")
        return id
    
    def updateSpecificDocumentFromCollection(self, idOfDocumentToUpdate: str, requestBody: dict) -> str:
        self.deleteBookById(idOfDocumentToUpdate)
        self._collection.append(requestBody)
        return idOfDocumentToUpdate
                
    def __isQueryParameterSatisfiedByDocument(self, document: dict, queryKey: str, queryValue: str) -> bool:
        documentValue = document[queryKey]
        # TODO: It won't be language. How does if influence (I think authors is also a list)??? Slide 19 is not clear
        if type(documentValue) is list:
            return queryValue in documentValue
        return documentValue == queryValue
            
        
            
        
        
