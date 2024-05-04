from flask_restful import Resource, reqparse
from Models.RatingsCollection import RatingsCollection
from Exceptions.NoMatchingItemException import NoMatchingItemException

# TODO: Should it be seperated from RatingId? Can I override the function in one class?
class Ratings(Resource):
    def __init__(self, ratingsCollection: RatingsCollection) -> None:
        self._ratingsCollection = ratingsCollection()
        self._parser = reqparse.RequestParser()
        self.__addArgumentsToParser()
        
    def get(self) -> tuple:
        query = self._parser.parse_args()
        print(f"Called get on Rating resource with query: {query}")
        # TODO: Input tests (dataValidator) - make sure query has id. What happens if there is other key instead/in addition to id?
        try: 
            id = query["id"]
            return self._ratingsCollection.getRatingById(id), 200
        
        except KeyError as exception:
            return "Id wasn't given in the query, got exception: " + exception.message, 422
        
        except NoMatchingItemException as exception:
            return "No matching item: " + exception.message, 404

        except Exception as exception:
            return "Unexpected error: " + exception.args[0], 500
        
    def __addArgumentsToParser(self) -> None:
        self._parser.add_argument('id', location='args', required=True)