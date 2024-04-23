# TODO: sort by a,b,c in all files, remove unneccesarry imports
# TODO: add return type to all functions
from Collections.BooksCollection import BooksCollection
from flask_restful import Resource
from flask import request

class Books(Resource):        
    def __init__(self, booksCollection: BooksCollection) -> None:
        self.booksCollection = booksCollection()
    
    def post(self) -> str:
        requestBody = request.get_json()
        postRequestBodyValidationResult = self.validatePostRequestBody(requestBody)
        
        if postRequestBodyValidationResult != "Valid post request body":
            return postRequestBodyValidationResult, 400
        
        title, ISBN, genre = requestBody["title"], requestBody["ISBN"], requestBody["genre"]
        newBookId = self.booksCollection.insertBookAndReturnId(title, ISBN, genre)
        
        return newBookId, 201
    
    
    # TODO: Should be here?
    def validatePostRequestBody(self, requestBody: dict) -> str:
        try:
            title = requestBody["title"]
        except KeyError:
            return "There is a missing title parameter in your request body"
        try:
            ISBN = requestBody["ISBN"]
        except KeyError:
            return "There is a missing ISBN parameter in your request body"
        try:
            genre = requestBody["genre"]
        except KeyError:
            return "There is a missing genre parameter in your request body"
        
        return "Valid post request body"