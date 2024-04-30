from flask import Flask
# TODO: are all those imports necessary?
from flask_restful import Api
from Resources.Books import Books
from Resources.Id import Id
from Resources.RatingId import RatingId
from Resources.Top import Top
from Resources.Values import Values
from Container import Container
from Models.BooksCollection import BooksCollection
# TODO: Check why the Provide isn't in use
from dependency_injector.wiring import Provide, inject

# TODO: Check why the @inject is for 
@inject
def main() -> None:
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(Books, '/books', resource_class_kwargs={'booksCollection': container.booksCollection, 'dataValidator': container.dataValidator})
    api.add_resource(Id, '/books/<string:id>', resource_class_kwargs={'booksCollection': container.booksCollection, 'dataValidator': container.dataValidator})
    api.add_resource(RatingId, '/rating/<string:id>', resource_class_kwargs={'ratingsCollection': container.ratingsCollection})
    api.add_resource(Top, '/top', resource_class_kwargs={'ratingsCollection': container.ratingsCollection})
    api.add_resource(Values, '//rating/<string:id>/values', resource_class_kwargs={'ratingsCollection': container.ratingsCollection})
    
    app.run(host='0.0.0.0', port=8000, debug=True)
    
if __name__ == '__main__':
    container = Container()
    container.wire(modules=[__name__])
    print("Running the server")
    main()
