from flask import request
from flask_restful import Resource
from Models.RatingsCollection import RatingsCollection
from Services.DataValidator import DataValidator
from Exceptions.InvalidRequestBodyException import InvalidRequestBodyException
from Exceptions.UnsupportedMediaTypeException import UnsupportedMediaTypeException

class Values(Resource):
    def __init__(self, ratingsCollection: RatingsCollection, dataValidator: DataValidator) -> None:
        self._ratingsCollection = ratingsCollection()
        self._dataValidator = dataValidator()
        
    def post(self, id: str) -> tuple:
        try:
            requestBody = request.get_json()
            print(f"Called POST on Values resource with requestBody: {requestBody}")
            self._dataValidator.validateValuesPostRequestBody(requestBody)
            value = requestBody["value"]
            print(f"Assigned value to: {value}")
            if not self._ratingsCollection.doRatingWithGivenIdAlreadyExist(id):
                raise InvalidRequestBodyException("A book with the given id doesn't exist in the ratings collection")
            print("Didn't throw exception")
            newAverage = self._ratingsCollection.addRatingValueToBookAndReturnNewAverage(id, value)
            print(f"newAverage is: {newAverage}")
            return newAverage, 201
        
        except InvalidRequestBodyException as exception:
            return "Unprocessable Content: " + exception.message, 422
        
        except UnsupportedMediaTypeException as exception:
            return "Unsupported media type: " + exception.message, 415
        
        except Exception as exception:
            print(exception.args)
            return "Unexpected error: " + exception.args, 500
    