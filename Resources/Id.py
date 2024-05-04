# TODO: Add readme
from Models.BooksCollection import BooksCollection
from flask_restful import Resource, reqparse
from dependency_injector.wiring import Provide, inject
from Exceptions.NoMatchingItemException import NoMatchingItemException
from Exceptions.InvalidRequestBodyException import InvalidRequestBodyException
from Exceptions.UnsupportedMediaTypeException import UnsupportedMediaTypeException
from Services.DataValidator import DataValidator
from flask import request

class Id(Resource):
    def __init__(self, booksCollection: BooksCollection, dataValidator: DataValidator) -> None:
        # TODO: Check if it creates another one
        # TODO: Should I add super.__init__()? Does it invoke it automatically if I don't have a constructor?
        self._booksCollection = booksCollection()
        self._dataValidator = dataValidator()
    
    def get(self, id: str) -> tuple:
        try:
            return self._booksCollection.getBookById(id), 200
        
        except NoMatchingItemException as exception:
            return "No matching item: " + exception.message, 404
        
        except Exception as exception:
            return "Unexpected error: " + exception.args[0], 500
        
    # TODO: Is this a tuple?
    def delete(self, id: str) -> tuple:
        print(f"Called DELETE on Id with id: {id}")
        try:
            deletedBookId = self._booksCollection.deleteBookById(id), 200
            return deletedBookId
        
        except NoMatchingItemException as exception:
            return "No matching item" + exception.message, 404
        
        except Exception as exception:
            return "Unexpected error: " + exception.args[0], 500
        
        
    def put(self, id: str) -> tuple:
        print(f"Called PUT on Id with id: {id}")
        try:
            requestBody = request.get_json()
            self._dataValidator.validateIdPutRequestBody(requestBody)
            updatedDocumentId = self._booksCollection.updateSpecificDocumentFromCollection(id, requestBody)
            return updatedDocumentId, 200
        
        except InvalidRequestBodyException as exception:
            return "Unprocessable content: " + exception.message, 422
        
        except NoMatchingItemException as exception:
            return "No matching item: " + exception.message, 404
        
        except UnsupportedMediaTypeException as exception:
            return "Unsupported media type: " + exception.message, 415
        
        except Exception as exception:
            return "Unexpected error: " + exception.args[0], 500
        # TODO: Except more errors
        # TODO: Check if errors like unparseable json which returns 405 should be handeled