# TODO: Check why he wrote that /books is a resource (slide 6), and also why /books is a collection of books and /ratings is a collection of book ratings
# TODO: sort by a,b,c in all files, remove unneccesarry imports
# TODO: add return type to all functions
from Collections.BooksCollection import BooksCollection
from Services.DataValidator import DataValidator
from flask_restful import Resource, reqparse
from flask import request
# TODO: Check if it should be here and not injected (I think it's good like that)
from Exceptions.InvalidRequestBodyException import InvalidRequestBodyException
from Exceptions.EmptyCollectionException import EmptyCollectionException

class Books(Resource):        
    def __init__(self, booksCollection: BooksCollection, dataValidator: DataValidator) -> None:
        # TODO: Check if it creates a new instance of booksCollection and dataValidator and why it's invoked
        # TODO: make all the fields private with providers
        self._booksCollection = booksCollection()
        self._dataValidator = dataValidator()
        self._parser = reqparse.RequestParser()
        self.__addArgumentsToParser()
    
    def post(self) -> str:
        print("Called post on Books resource")
        try:
            requestBody = request.get_json()
            self._dataValidator.validateBooksPostRequestBody(requestBody)
            newBookId = self._booksCollection.insertBookAndReturnId(requestBody)    
            return newBookId, 201
        
        except InvalidRequestBodyException as error:
            return "Bad request: " + error.message, 400
        # TODO: Except more specific errors
        # TODO: Check if errors like unparseable json which returns 405 should be handeled
            
    def get(self) -> str:
        # TODO: Input tests (query is valid for example)
        try:
            print("Called get on Books resource")
            query = self._parser.parse_args()
            collection = self._booksCollection.getCollectionFilteredByQuery(query)
            if collection == []:
                # TODO: should it be 204 (The request was successful but the response has no content)?
                return "There aren't books matching your criteria", 404
            return collection, 200
        except EmptyCollectionException as error:
            return error.message, 404
    
    def __addArgumentsToParser(self):
        self._parser.add_argument('title', location='args', required=False)
        self._parser.add_argument('ISBN', location='args', required=False)
        self._parser.add_argument('genre', location='args', required=False)
        self._parser.add_argument('authors', location='args', required=False)
        self._parser.add_argument('publisher', location='args', required=False)
        self._parser.add_argument('publishedDate', location='args', required=False)
        self._parser.add_argument('id', location='args', required=False)
        self._parser.add_argument('language', location='args', required=False)
        self._parser.add_argument('summary', location='args', required=False)