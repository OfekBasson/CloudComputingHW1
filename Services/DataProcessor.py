import uuid
from Services.ApiInvoker import ApiInvoker
from Exceptions.NoMatchingItemsInApiGetCallException import NoMatchingItemsInApiGetCallException
from Exceptions.InternalServerException import InternalServerException
from datetime import datetime

class DataProcessor():
    
    def __init__(self, apiInvoker: ApiInvoker) -> None:
        self._apiInvoker = apiInvoker
    
    # TODO: Check if a book already exists
    def constructFullBookData(self, partialBookData: dict) -> dict:
        print(f"Inside 'constructFullBookData'. Constructing foll data to partialBookData: {partialBookData}")
        # TODO: Handle missing data (slide 14)
        try:
            isbn = partialBookData["ISBN"]            
            
            # TODO: add asynchronous handling
            # bookData, language, summary = await asyncio.gather((self.__getBookData(isbn), self.__getLanguage(isbn), self.__getBookSummary(partialBookData["title"], bookData["authors"])))
            bookData = self.__getBookData(isbn)
            language = self.__getLanguage(isbn)
            summary = self.__getBookSummary(partialBookData["title"], bookData["authors"])

            fullData = self.__combineDataFromRequestAndApiCalls(partialBookData, bookData, language, summary)
            self.__postProcessData(fullData)
            
            return fullData
            
        # TODO: Change handling to more specific row... return something
        except Exception as exception:
            raise InternalServerException(f"Unable to construct full data for partial book data {partialBookData}. Exception is: {exception.args[0]}")
        
    def __combineDataFromRequestAndApiCalls(self, requestBody: dict, bookData: dict, language: list, summary: str) -> dict:
        print(f"Inside '__combineDataFromRequestAndApiCalls' (private function of DataProcessor) with requestBody: {requestBody}, bookData: {bookData}, language: {language} and summary: {summary}")
        fullData = dict(requestBody)
        fullData.update(bookData)
        fullData["id"] = str(uuid.uuid4())            
        fullData["language"] = language
        fullData["summary"] = summary        
        
        return fullData
    
    def __getBookData(self, isbn: str) -> dict:
        print(f"Inside '__getBookData' (private function of DataProcessor) with ISBN: {isbn}")
        try:
            bookData = self._apiInvoker.sendGetRequestToGoogleBooksApiAndReturnBookData(isbn)
            for key in bookData:
                if bookData[key] == "":
                    bookData[key] = "missing"
        except NoMatchingItemsInApiGetCallException as exception:
            bookData = {
            "authors": "missing",
            "publisher": "missing",
            "publishedDate": "missing"
            }
            # TODO: add logs?
        return bookData
    
    def __getLanguage(self, isbn: str) -> list:
        print(f"Inside '__getLanguage' (private function of DataProcessor) with ISBN: {isbn}")
        try:
            language = self._apiInvoker.sendGetRequestToOpenApiLibraryAndReturnLanguages(isbn)
        except NoMatchingItemsInApiGetCallException:
            language = ["missing"]
            # TODO: add logs?
        return language
    
    # TODO: Add type for title and authors
    def __getBookSummary(self, title: str, authors: list) -> str:
        print(f"Inside '__getBookSummary' (private function of DataProcessor) with title: {title} and authors: {authors}")
        try:
            firstAuthorName = authors[0]
            bookSummary = self._apiInvoker.sendGetRequestToGoogleGenAIAndReturnBookSummary(title, firstAuthorName)
        except NoMatchingItemsInApiGetCallException:
            bookSummary = "missing"
            # TODO: add logs?
        return bookSummary   
    
    def __postProcessData(self, data: dict) -> None:
        print(f"Inside '__postProcessData (private function of DataProcessor) with data: {data}")
        data["publishedDate"] = self.__getValidDate(data["publishedDate"])
        data["authors"] = self.__concatenateListToString(data["authors"])
        # TODO: Implement
        return 
    
    def __getValidDate(self, dateString: str) -> str:
        print(f"Inside '__getValidDate' (private function of DataProcessor) with dateString: {dateString}")
        formats = ["%Y-%m-%d", "%Y"]
        for format in formats:
            try:
                datetime.strptime(dateString, format)
                return dateString
            except ValueError:
                pass
        return "missing"
    
    def __concatenateListToString(self, listToConcatenate: list) -> str:
        print(f"Inside '__concatenateLanguagesToString' (private function of DataProcessor) with listToConcatenate: {listToConcatenate}")
        return " and ".join(listToConcatenate)