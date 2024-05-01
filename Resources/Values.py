from flask_restful import Resource
from Models.RatingsCollection import RatingsCollection
from Services.DataValidator import DataValidator
from Exceptions.InvalidRequestBodyException import InvalidRequestBodyException
from Exceptions.UnsupportedMediaTypeException import UnsupportedMediaTypeException
from flask import request

class Values(Resource):
    def __init__(self, ratingsCollection: RatingsCollection, dataValidator: DataValidator) -> None:
        self._ratingsCollection = ratingsCollection
        self._dataValidator = dataValidator
        
    def post(self, id: str) -> tuple:
        # TODO: Get data as payload
        # TODO: Implement
        try:
            requestBody = request.get_json()
            self._dataValidator.validateValuesPostRequestBody(requestBody)
            value = requestBody["value"]
            if not self._ratingsCollection.doRatingWithGivenIdAlreadyExist(requestBody["id"]):
                # TODO: Is this the exception which has to be thrown?
                raise InvalidRequestBodyException("A book with the same id doesn't exist in the collection")
            newAverage = self._ratingsCollection.addRatingValueToBookAndReturnNewAverage(id, value)
            return newAverage, 201
        
        except InvalidRequestBodyException as exception:
            return "Unprocessable Content: " + exception.message, 422
        
        except UnsupportedMediaTypeException as exception:
            return "Unsupported media type: " + exception.message, 415
        
        # TODO: Should I get Internal server exception here?