from Services.ApiInvoker import ApiInvoker
# TODO: What is Provide and inject for?
from dependency_injector.wiring import Provide, inject
from Exceptions.NoMatchingItemsInApiGetCallException import NoMatchingItemsInApiGetCallException
from Exceptions.EmptyCollectionException import EmptyCollectionException
from Services.DataProcessor import DataProcessor

class BooksCollection():
    # TODO: Is this a good practice to return None from constructor?
    def __init__(self, DataProcessor: DataProcessor) -> None:
        # TODO: Add reference to numberOfOperations in every operation
        self._numberOfOperationsSoFar = 0
        self._collection = []
        # TODO: should I add underscore before variable name?
        self._dataProcessor = DataProcessor
        
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
        except NoMatchingItemsInApiGetCallException as error:
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
                collectionCopy = list(filter(lambda document: self.isQueryParameterSatisfiedByDocument(document, queryKey, queryValue), collectionCopy))
                print(f"Finished filtering for '{queryKey}': '{queryValue}'. There are {len(collectionCopy)} books which matches the criteria so far")
        
        if len(collectionCopy) == 0:
            raise EmptyCollectionException("There are no books matching your criteria")
        
        return collectionCopy
                
    def isQueryParameterSatisfiedByDocument(self, document: dict, queryKey: str, queryValue: str) -> bool:
        documentValue = document[queryKey]
        if type(documentValue) is list:
            return queryValue in documentValue
        return documentValue == queryValue
            
        
            
        
        
