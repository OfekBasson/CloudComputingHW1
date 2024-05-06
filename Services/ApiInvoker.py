import requests
from Exceptions.NoMatchingItemsInApiGetCallException import NoMatchingItemsInApiGetCallException
from Exceptions.InternalServerException import InternalServerException
import google.generativeai as genai
import os

class ApiInvoker:
    def sendGetRequestToGoogleBooksApiAndReturnBookData(self, isbn: str) -> dict:
        print(f"inside 'sendGetRequestToGoogleBooksApiAndReturnBookData'. Invoking an api call with ISBN:{isbn}")
        googleBooksUrl = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}'
        response = requests.get(googleBooksUrl)
        try:
            googleBooksData = response.json()['items'][0]['volumeInfo']
            print(f'googleBooksData is: {googleBooksData}')
        except Exception as exception:
            print(f'exception is: {exception.args} and response.json is: {((response.json())["totalItems"]) == 0}')
            if ((response.json())["totalItems"]) == 0:
                raise NoMatchingItemsInApiGetCallException(f"No items returned from Google Book API for given ISBN number ({isbn})")
            if exception == "unable to connect to Google":
                raise InternalServerException("Unable to connect to google") 
            raise exception       
                
        bookData = {
        "authors": googleBooksData.get("authors"),
        "publisher": googleBooksData.get("publisher"),
        "publishedDate": googleBooksData.get("publishedDate")
        }
        
        return bookData
    
    def sendGetRequestToOpenApiLibraryAndReturnLanguages(self, isbn: str) -> list:
        print(f"inside 'sendGetRequestToOpenApiLibraryAndReturnLanguages'. Invoking an api call with ISBN:{isbn}")
        try:
            openApiLibraryUrl = f'https://openlibrary.org/search.json?q={isbn}&fields=key,title,author_name,language'
            response = requests.get(openApiLibraryUrl)
            language = response.json()['docs'][0]['language']
            return language
        except Exception as exception:
            if response.json()['numFound'] == 0:
                raise NoMatchingItemsInApiGetCallException(f"No items returned from OpenApiLibrary for given ISBN number ({isbn})")
            raise exception
            
    def sendGetRequestToGoogleGenAIAndReturnBookSummary(self, bookName: str, authorName: str) -> str:
        print(f"inside 'sendGetRequestToOpenApiLibraryAndReturnLanguages'. Invoking an api call with bookName:{bookName} and authorName: {authorName}")
        try:
            genai.configure(api_key=os.environ["API_KEY"])
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = f'Summarize the book {bookName} by {authorName} in 5 sentences or less.' if authorName != "missing" else f'Summarize the book {bookName} in 5 sentences or less.'
            response = model.generate_content(prompt)
            summary = response.text
            return summary 
        except Exception as exception:
            if exception == "unable to connect to Gemini":
                raise InternalServerException(exception)  
            raise exception

        
            


    