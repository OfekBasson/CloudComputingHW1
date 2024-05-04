# TODO: Check why he wrote that /books is a resource (slide 6), and also why /books is a collection of books and /ratings is a collection of book ratings
# TODO: sort by a,b,c in all files, remove unneccesarry imports
# TODO: add return type to all functions
from Models.BooksCollection import BooksCollection
from Services.DataValidator import DataValidator
from flask_restful import Resource, reqparse
from flask import request
# TODO: Check if it should be here and not injected (I think it's good like that)
from Exceptions.InvalidRequestBodyException import InvalidRequestBodyException
from Exceptions.UnsupportedMediaTypeException import UnsupportedMediaTypeException
from Exceptions.InternalServerException import InternalServerException
from Exceptions.EmptyCollectionException import EmptyCollectionException

class Books(Resource):        
    def __init__(self, booksCollection: BooksCollection, dataValidator: DataValidator) -> None:
        # TODO: Check if it creates a new instance of booksCollection and dataValidator and why it's invoked
        # TODO: make all the fields private with providers
        self._booksCollection = booksCollection()
        self._dataValidator = dataValidator()
        self._parser = reqparse.RequestParser()
        self.__addArgumentsToParser()
    
    def post(self) -> tuple:
        # TODO: Should a book which was entered twice appear twice in the booksCollection?
        try:
            requestBody = request.get_json(silent=True)
            print(f"Called post on Books resource with requestBodu: {requestBody}")
            self._dataValidator.validateBooksPostRequestBody(requestBody)
            if self._booksCollection.doBookWithGivenIsbnAlreadyExist(requestBody["ISBN"]):
                raise InvalidRequestBodyException("A book with the same ISBN already exist in the collection")
            newBookId = self._booksCollection.insertBookAndReturnId(requestBody)
            return newBookId, 201
        
        except InvalidRequestBodyException as exception:
            return "Unprocessable Content: " + exception.message, 422
        
        except UnsupportedMediaTypeException as exception:
            return "Unsupported media type: " + exception.message, 415
        
        except InternalServerException as exception:
            return "Internal server error: " + exception.message, 500
        
        except Exception as exception:
            return "Unexpected error: " + exception.args[0], 500
        # TODO: Except more specific errors
        # TODO: Check if errors like unparseable json which returns 405 should be handeled
            
    def get(self) -> tuple:
        try:
            query = self._parser.parse_args()
            print(f"Called GET on Books resource with query: {query}")
            # TODO: Input tests (query isn't valid for example, only one string in language/authors/,,,)
            collection = self._booksCollection.getCollectionFilteredByQuery(query)
            return collection, 200
        
        except EmptyCollectionException as exception:
            return "Empty collection: " + exception.message, 404
        
        except InternalServerException as exception:
            return "Internal server error: " + exception.message, 500
        # TODO: Should I differ Unexpected error from InternalServerError?
        
        except Exception as exception:
            print(exception)
            return "Unexpected error: ", 500
    # TODO: How do null enter the collection?
    def __addArgumentsToParser(self) -> None:
        self._parser.add_argument('title', location='args', required=False)
        self._parser.add_argument('ISBN', location='args', required=False)
        self._parser.add_argument('genre', location='args', required=False)
        self._parser.add_argument('authors', location='args', required=False)
        self._parser.add_argument('publisher', location='args', required=False)
        self._parser.add_argument('publishedDate', location='args', required=False)
        self._parser.add_argument('id', location='args', required=False)
        # TODO: Remove. it won't be language/summary
        self._parser.add_argument('language', location='args', required=False)
        self._parser.add_argument('summary', location='args', required=False)