# TODO: Check why he wrote that /books is a resource (slide 6)
# TODO: sort by a,b,c in all files, remove unneccesarry imports
# TODO: add return type to all functions
from Collections.BooksCollection import BooksCollection
from Services.DataValidator import DataValidator
from flask_restful import Resource
from flask import request
# TODO: Check if it should be here and not injected (I think it's good like that)
from Exceptions.InvalidRequestBodyException import InvalidRequestBodyException

class Books(Resource):        
    def __init__(self, booksCollection: BooksCollection, dataValidator: DataValidator) -> None:
        # TODO: Check if it creates a new instance of booksCollection and dataValidator
        self.booksCollection = booksCollection()
        self.dataValidator = dataValidator()
    
    def post(self) -> str:
        try:
            requestBody = request.get_json()
            self.dataValidator.validateBooksPostRequestBody(requestBody)
            newBookId = self.booksCollection.insertBookAndReturnId(requestBody)    
            return newBookId, 201
        
        except InvalidRequestBodyException as error:
            return "Bad request: " + error.message, 400
            

        # TODO: Except more specific errors
        # TODO: Check if errors like unparseable json which returns 405 should be handeled
            
    def get(self) -> str:
        return self.booksCollection.collection