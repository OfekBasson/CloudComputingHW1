from flask import Flask
# TODO: are all those imports necessary?
from flask_restful import Api
from Routes.Books import Books
from Routes.Id import Id
from Collections.BooksCollection import BooksCollection
from Container import Container
from dependency_injector.wiring import Provide, inject

# TODO: Check why the @inject is for
@inject
def main() -> None:
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(Books, '/books', resource_class_kwargs={'booksCollection': container.booksCollection})
    api.add_resource(Id, '/books/id', resource_class_kwargs={'booksCollection': container.booksCollection})
    
    app.run(host='0.0.0.0', port=8000, debug=True)
    
if __name__ == '__main__':
    container = Container()
    container.wire(modules=[__name__])
    print("Running the server")
    main()
