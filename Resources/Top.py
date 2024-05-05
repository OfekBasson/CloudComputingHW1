from flask_restful import Resource
from Models.RatingsCollection import RatingsCollection

class Top(Resource):
    # TODO: He asked in slide 26 that "The books in the array have the top scores out of all the books". I don't store it as a seperate colection
    def __init__(self, ratingsCollection: RatingsCollection) -> None:
        self._ratingsCollection = ratingsCollection()
        
    def get(self) -> tuple:
        print("Called GET on Top resource")
        try:
            return self._ratingsCollection.getTopRatedBooks(), 200
        except:
            # TODO: Implement exception handling
            pass