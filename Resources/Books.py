from Models.BooksCollection import BooksCollection
from Services.DataValidator import DataValidator
from flask_restful import Resource, reqparse
from flask import request
from Exceptions.InvalidRequestBodyException import InvalidRequestBodyException
from Exceptions.UnsupportedMediaTypeException import UnsupportedMediaTypeException
from Exceptions.InternalServerException import InternalServerException
from Exceptions.EmptyCollectionException import EmptyCollectionException
from Exceptions.NoMatchingItemsInApiGetCallException import NoMatchingItemsInApiGetCallException

class Books(Resource):        
    def __init__(self, booksCollection: BooksCollection, dataValidator: DataValidator) -> None:
        self._booksCollection = booksCollection()
        self._dataValidator = dataValidator()
        self._parser = reqparse.RequestParser()
        self.__addArgumentsToParser()
    
    def post(self) -> tuple:
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
        
        except NoMatchingItemsInApiGetCallException as exception:
            return "No matching itemd in api get call: " + exception.message, 422
        
        except UnsupportedMediaTypeException as exception:
            return "Unsupported media type: " + exception.message, 415
        
        except InternalServerException as exception:
            return "Internal server error: " + exception.message, 500
        
        except Exception as exception:
            return "Unexpected error: " + exception.args, 500
            
    def get(self) -> tuple:
        try:
            query = self._parser.parse_args()
            print(f"Called GET on Books resource with query: {query}")
            collection = self._booksCollection.getCollectionFilteredByQuery(query)
            return collection, 200
        
        except EmptyCollectionException as exception:
            return "Empty collection: " + exception.message, 404
        
        except InternalServerException as exception:
            return "Internal server error: " + exception.message, 500
        
        except InvalidRequestBodyException as exception:
            return "Unprocessable Content: " + exception.message, 422
        
        except Exception as exception:
            print(exception)
            return "Unexpected error: ", 500

    def __addArgumentsToParser(self) -> None:
        self._parser.add_argument('title', location='args', required=False)
        self._parser.add_argument('ISBN', location='args', required=False)
        self._parser.add_argument('genre', location='args', required=False)
        self._parser.add_argument('authors', location='args', required=False)
        self._parser.add_argument('publisher', location='args', required=False)
        self._parser.add_argument('publishedDate', location='args', required=False)
        self._parser.add_argument('id', location='args', required=False)
        self._parser.add_argument('language', location='args', required=False)
