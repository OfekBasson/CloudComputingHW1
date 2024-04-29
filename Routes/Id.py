# TODO: Add readme, .gitignore
from Collections.BooksCollection import BooksCollection
from flask_restful import Resource, reqparse
from dependency_injector.wiring import Provide, inject
from Exceptions.NoMatchingItemException import NoMatchingItemException
from Exceptions.InvalidRequestBodyException import InvalidRequestBodyException
from Services.DataValidator import DataValidator
from flask import request

class Id(Resource):
    def __init__(self, booksCollection: BooksCollection, dataValidator: DataValidator) -> None:
        # TODO: Check if it creates another one
        self._booksCollection = booksCollection()
        self._dataValidator = dataValidator()
    
    def get(self, id: str) -> tuple:
        try:
            return self._booksCollection.getBookById(id), 200
        # TODO: Change from "error" to "exception"
        except NoMatchingItemException as error:
            return error.message, 404
        
    # TODO: Is this a tuple?
    def delete(self, id: str) -> tuple:
        try:
            deletedBookId = self._booksCollection.deleteBookById(id), 200
            return deletedBookId
        except NoMatchingItemException as error:
            return error.message, 404
        
    def put(self, id: str) -> tuple:
        try:
            requestBody = request.get_json()
            self._dataValidator.validateIdPutRequestBody(requestBody)
            updatedDocumentId = self._booksCollection.updateSpecificDocumentFromCollection(id, requestBody)
            return updatedDocumentId, 200
        except InvalidRequestBodyException as error:
            return "Bad request: " + error.message, 400
        except NoMatchingItemException as error:
            return error.message, 404
        # TODO: Except more specific errors
        # TODO: Check if errors like unparseable json which returns 405 should be handeled