from Services.ApiInvoker import ApiInvoker
# TODO: What is Provide and inject for?
from dependency_injector.wiring import Provide, inject
from Exceptions.NoMatchingItemsInApiGetCallException import NoMatchingItemsInApiGetCallException
from Services.RequestsDataHandler import RequestsDataHandler

class BooksCollection():
    # TODO: Is this a good practice to return None from constructor?
    def __init__(self, requestsDataHandler: RequestsDataHandler) -> None:
        self.numberOfOperationsSoFar = 0
        self.collection = []
        # TODO: should I add underscore before variable name?
        self.requestsDataHandler = requestsDataHandler
        
    # TODO: Change to "retreiveDataAndInsert..."" and split the retrieving and the insertion
    def insertBookAndReturnId(self, requestBody: dict) -> str:
        # TODO: Add logic here
        try:
            self.numberOfOperationsSoFar += 1
            requestWithFullData = self.requestsDataHandler.handlePostRequestToBooks(requestBody)
            self.collection.append(requestWithFullData)
            id = requestWithFullData["id"]
            return id
        except NoMatchingItemsInApiGetCallException as error:
            return requestBody
        
        
