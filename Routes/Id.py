# TODO: Add readme, .gitignore
from Collections.BooksCollection import BooksCollection
from flask_restful import Resource, reqparse
from dependency_injector.wiring import Provide, inject

class Id(Resource):
    def __init__(self, booksCollection: BooksCollection) -> None:
        self.booksCollection = booksCollection()
    
    def get(self) -> str:
        return "", 200
    