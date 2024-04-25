import uuid
from Services.ApiInvoker import ApiInvoker

class RequestsDataHandler():
    
    def __init__(self, apiInvoker: ApiInvoker) -> None:
        self.apiInvoker = apiInvoker
    
    def handlePostRequestToBooks(self, requestBody) -> dict:
        # TODO: Handle missing data (slide 14)
        try:
            isbn = requestBody["ISBN"]            
            bookData = self.apiInvoker.sendGetRequestToGoogleBooksApiAndReturnBookData(isbn)
            language = self.apiInvoker.sendGetRequestToOpenApiLibraryAndReturnLanguages(isbn)
            summary = self.apiInvoker.sendGetRequestToGOogleGenAIAndReturnBookSummary(requestBody["title"], bookData["authors"])

            requestWithFullData = dict(requestBody)
            requestWithFullData.update(bookData)
            requestWithFullData["id"] = str(uuid.uuid4())            
            requestWithFullData["language"] = language
            requestWithFullData["summary"] = summary
            
            return requestWithFullData
            
        # TODO: Change handling to more specific row...
        except Exception as error:
            print(error)
            pass
        
        