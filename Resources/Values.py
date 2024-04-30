from flask_restful import Resource
from Models.RatingsCollection import RatingsCollection

class Values(Resource):
    def __init__(self, ratingsCollection: RatingsCollection) -> None:
        self._ratingsCollection = ratingsCollection
        
    def post(self) -> tuple:
        # TODO: Get data as payload
        # TODO: Implement
        try:
            return self._ratingsCollection.addRatingValueToBookAndReturnNewAverage(id, value), 200
        except:
            # TODO: Implement exception handling
            pass