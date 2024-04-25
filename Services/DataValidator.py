# TODO: Check if it should be here and not injected (I think it's good like that)
from Exceptions.InvalidRequestBodyException import InvalidRequestBodyException

class DataValidator:
    def validateBooksPostRequestBody(self, requestBody: dict) -> str:
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
        if len(requestBody) >= 4:
            raise InvalidRequestBodyException("The request body length is greater than 3 (should be only 3 - title, ISBN, genre)")
        
        return "Valid post request body"