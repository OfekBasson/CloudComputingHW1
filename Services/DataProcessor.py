import uuid
from Services.ApiInvoker import ApiInvoker
from Exceptions.NoMatchingItemsInApiGetCallException import NoMatchingItemsInApiGetCallException

class DataProcessor():
    
    def __init__(self, apiInvoker: ApiInvoker) -> None:
        self._apiInvoker = apiInvoker
    
    # TODO: Check if a book already exists
    def constructFullBookData(self, partialBookData: dict) -> dict:

        # TODO: Handle missing data (slide 14)
        try:
            isbn = partialBookData["ISBN"]            
            
            bookData = self.__getBookData(isbn)
            language = self.__getLanguage(isbn)
            summary = self.__getBookSummary(partialBookData["title"], bookData["authors"])

            fullData = self.__combineDataFromRequestAndApiCalls(partialBookData, bookData, language, summary)
            
            return fullData
            
        # TODO: Change handling to more specific row... return something
        except Exception as error:
            print(error)
            pass
        
    def __combineDataFromRequestAndApiCalls(self, requestBody: dict, bookData: dict, language: list, summary: str) -> dict:
        fullData = dict(requestBody)
        fullData.update(bookData)
        fullData["id"] = str(uuid.uuid4())            
        fullData["language"] = language
        fullData["summary"] = summary        
        
        return fullData
    
    def __getBookData(self, isbn: str) -> dict:
        try:
            bookData = self._apiInvoker.sendGetRequestToGoogleBooksApiAndReturnBookData(isbn)
            for key in bookData:
                if bookData[key] == "":
                    bookData[key] = "missing"
        except NoMatchingItemsInApiGetCallException as error:
            bookData = {
            "authors": "missing",
            "publisher": "missing",
            "publishedDate": "missing"
            }
            # TODO: add logs?
        return bookData
    
    def __getLanguage(self, isbn: str) -> list:
        try:
            language = self._apiInvoker.sendGetRequestToOpenApiLibraryAndReturnLanguages(isbn)
        except NoMatchingItemsInApiGetCallException:
            language = ["missing"]
            # TODO: add logs?
        return language
    
    # TODO: Add type for title and authors
    def __getBookSummary(self, title: str, authors: list) -> str:
        try:
            firstAuthorName = authors[0]
            bookSummary = self._apiInvoker.sendGetRequestToGOogleGenAIAndReturnBookSummary(title, firstAuthorName)
        except NoMatchingItemsInApiGetCallException:
            bookSummary = "missing"
            # TODO: add logs?
        return bookSummary        
        