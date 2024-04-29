# TODO: Check if it should be here and not injected (I think it's good like that)
from Exceptions.InvalidRequestBodyException import InvalidRequestBodyException
# TODO: Add interfaces
# TODO: Change to another name? maybe RequestBodyValidator?
class DataValidator:
    def validateBooksPostRequestBody(self, requestBody: dict) -> str:
        if len(requestBody) >= 4:
            raise InvalidRequestBodyException("The request body length is greater than 3 (should be only 3 - title, ISBN, genre)")
        try:
            title = requestBody["title"]
        except KeyError:
            raise InvalidRequestBodyException("There is a missing title parameter in your request body")
        try:
            ISBN = requestBody["ISBN"]
        except KeyError:
            raise InvalidRequestBodyException("There is a missing ISBN parameter in your request body")
        try:
            genre = requestBody["genre"]
        except KeyError:
            raise InvalidRequestBodyException("There is a missing genre parameter in your request body")
        
        return "Valid post request body"
    
    def validateIdPutRequestBody(self, requestBody: dict) -> str:
        # TODO: Check if the id of the new item equals the changed id
        try:
            for key in ["title", "ISBN", "genre", "publisher", "publishedDate", "id", "summary"]:
                if type(requestBody[key]) is not str:
                    raise InvalidRequestBodyException('One of the provided keys which supposed to be string ("title", "ISBN", "genre", "publisher", "publishedDate", "id", "summary") is not a string')
            for key in ["authors", "language"]:
                if type(requestBody[key]) is not list:
                    raise InvalidRequestBodyException('One of the provided keys which supposed to be list ("language", "authors") is not a list')
        except KeyError as error:
            raise InvalidRequestBodyException('One of the required fields doesnt exist in the request ("title", "ISBN", "genre", "publisher", "publishedDate", "id", "summary", "language", "authors")')
        
        return "Valid put request body"