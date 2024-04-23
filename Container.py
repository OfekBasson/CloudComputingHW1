# TODO: Check where all my dependencies are (should be in the docker container)
from dependency_injector import containers, providers
from Collections.BooksCollection import BooksCollection

class Container(containers.DeclarativeContainer):

    # config = providers.Configuration()

    booksCollection = providers.Singleton(
        BooksCollection
    )
    
