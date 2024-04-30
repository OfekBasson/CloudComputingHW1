from flask_restful import Resource
from Models.RatingsCollection import RatingsCollection

class RatingId(Resource):
    def __init__(self, ratingsCollection: RatingsCollection) -> None:
        self._ratingsCollection = ratingsCollection
        
    def get(self, id: str) -> tuple:
        try:
            return self._ratingsCollection.getRatingIdJson(id), 200
        except:
            # TODO: Implement exception handling
            pass