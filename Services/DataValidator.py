# TODO: Check if it should be here and not injected (I think it's good like that)
from Exceptions.InvalidRequestBodyException import InvalidRequestBodyException
from Exceptions.UnsupportedMediaTypeException import UnsupportedMediaTypeException
from Exceptions.InternalServerException import InternalServerException
# TODO: Add interfaces
# TODO: Change to another name? maybe RequestBodyValidator?
class DataValidator:    
    def validateBooksPostRequestBody(self, requestBody: dict) -> None:
        # TODO: Check if I can return this also if requestBody is actually None and not only if it's unsupported media type
        if requestBody is None:
            raise UnsupportedMediaTypeException("The request body is None or has unsupported type")
        # TODO: Doesn't appear in the instructions. Make sure that it's ok
        if len(requestBody) >= 4:
            raise InvalidRequestBodyException("The request body length is greater than 3 (should be only 3 - title, ISBN, genre)")
        # TODO: How to handle capital letters as keys (for example "Title")?
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
        if genre not in ['Fiction', 'Children', 'Biography', 'Science', 'Science Fiction', 'Fantasy', 'Other']:
            raise InvalidRequestBodyException(f"The genre ({genre}) isn't valid")
        
        print(f"Inside 'validateBooksPostRequestBody' (function of 'DataValidator') the data is valid ({requestBody})")
    
    def validateIdPutRequestBody(self, requestBody: dict) -> None:
        # TODO: Check if the id of the new item equals the changed id
        # TODO: How to handle capital letters as keys (for example "Title")?
        try:
            if requestBody is None:
                raise UnsupportedMediaTypeException("The request body is None or has unsupported type")
            for key in ["title", "ISBN", "genre", "publisher", "publishedDate", "id", "summary"]:
                if type(requestBody[key]) is not str:
                    raise InvalidRequestBodyException('One of the provided keys which supposed to be string ("title", "ISBN", "genre", "publisher", "publishedDate", "id", "summary") is not a string')
            # TODO: It won't be summary/language. How does it influence the code?
            for key in ["authors", "language"]:
                if type(requestBody[key]) is not list:
                    raise InvalidRequestBodyException('One of the provided keys which supposed to be list ("language", "authors") is not a list')
            if requestBody["genre"] not in ['Fiction', 'Children', 'Biography', 'Science', 'Science Fiction', 'Fantasy', 'Other']:
                raise InvalidRequestBodyException(f"The genre ({requestBody["genre"]}) isn't valid")
        except KeyError as exception:
            raise InvalidRequestBodyException('One of the required fields doesnt exist in the request ("title", "ISBN", "genre", "publisher", "publishedDate", "id", "summary", "language", "authors")')
        print(f"Inside 'validateIdPutRequestBody' (function of 'DataValidator') the data is valid ({requestBody})")
    
    def validateDataForCreateNewRating(self, data: dict) -> None:
        try:
            title = data["title"]
        except KeyError:
            raise InternalServerException("Unexpected exception: no title field in the data provided to 'createNewRating' (function of RatingsCollection)")
        try:
            id = data["id"]
        except KeyError:
            raise InternalServerException("Unexpected exception: no id field in the data provided to 'createNewRating' (function of RatingsCollection)")
        print(f"Inside 'validateDataForCreateNewRating' (function of 'DataValidator') the data is valid ({data})")

    def validateValuesPostRequestBody(self, requestBody: dict) -> None:
        if requestBody is None:
            raise UnsupportedMediaTypeException("The request body is None or has unsupported type")
        if len(requestBody) >= 1:
            raise InvalidRequestBodyException("The request body length is greater than 1 (should be only 1 - id)")
        try:
            # TODO: Check it's int (is it possible to parse the request body to int?)
            value = requestBody["value"]
        except KeyError:
            raise InvalidRequestBodyException("The value parameter is missing from your request body")
        if value not in [1, 2, 3, 4, 5]:
            raise InvalidRequestBodyException(f"The value ({value}) isn't valid")
        
        print(f"Inside 'validateValuesPostRequestBody' (function of 'DataValidator') the data is valid ({requestBody})")
        