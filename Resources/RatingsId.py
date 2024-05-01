from flask_restful import Resource
from Models.RatingsCollection import RatingsCollection
from Exceptions.NoMatchingItemException import NoMatchingItemException

class RatingsId(Resource):
    def __init__(self, ratingsCollection: RatingsCollection) -> None:
        self._ratingsCollection = ratingsCollection
        
    def get(self, id: str) -> tuple:
        print("Called get on RatingId resource")
        try:
            return self._ratingsCollection.getRatingById(id), 200
        except NoMatchingItemException as exception:
            return "No matching item: " + exception.message, 404
        except Exception as exception:
            return "Internal server error: " + exception.message, 500