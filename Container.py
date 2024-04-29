# TODO: Check where all my dependencies are (should be in the docker container)
from dependency_injector import containers, providers
from Collections.BooksCollection import BooksCollection
from Services.DataValidator import DataValidator
from Services.ApiInvoker import ApiInvoker
from Services.DataProcessor import DataProcessor

class Container(containers.DeclarativeContainer):
    # TODO: Add urls to config
    # config = providers.Configuration()

    apiInvoker = providers.Singleton(
        ApiInvoker
    )
    
    dataProcessor = providers.Singleton(
        DataProcessor,
        apiInvoker=apiInvoker
    )
    
    booksCollection = providers.Singleton(
        BooksCollection,
        DataProcessor=dataProcessor
    )
    
    dataValidator = providers.Singleton(
        DataValidator
    )
    
