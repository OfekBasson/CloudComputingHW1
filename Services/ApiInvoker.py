import requests
from Exceptions.NoMatchingItemsInApiGetCallException import NoMatchingItemsInApiGetCallException
import google.generativeai as genai
import os

class ApiInvoker:
    
    def sendGetRequestToGoogleBooksApiAndReturnBookData(self, isbn: str) -> dict:
        googleBooksUrl = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}'
        response = requests.get(googleBooksUrl)
        try:
            googleBooksData = response.json()['items'][0]['volumeInfo']
        # TODO: Check why the status code should be 200 and where he wrote it (the status code he provided is 400)
        # TODO: Raise exception here and catch it somewhere - I have to get an approval tor this
        # dmy: if no items returned, this line throws an exception "no items" but the return status code is still 200
        except:
            if response.json()['totalItems'] == 0:
                raise NoMatchingItemsInApiGetCallException(f"No items returned from Google Book API for given ISBN number ({isbn})")
        
        bookData = {
        "authors": googleBooksData.get("authors"),
        "publisher": googleBooksData.get("publisher"),
        "publishedDate": googleBooksData.get("publishedDate")
        }
        
        return bookData
    
    def sendGetRequestToOpenApiLibraryAndReturnLanguages(self, isbn: str) -> list:
        try:
            openApiLibraryUrl = f'https://openlibrary.org/search.json?q={isbn}&fields=key,title,author_name,language'
            response = requests.get(openApiLibraryUrl)
            # TODO: Check if I should only get the 0 item/combining all documents languages
            language = response.json()['docs'][0]['language']
            return language
        except:
            if response.json()['numFound'] == 0:
                raise NoMatchingItemsInApiGetCallException(f"No items returned from OpenApiLibrary for given ISBN number ({isbn})")
        # TODO: Change the empty return. Maybe the return should be at the end of the function
        return []
            
    def sendGetRequestToGOogleGenAIAndReturnBookSummary(self, bookName: str, authorName: str) -> str:
        try:
            # TODO: Where is it recommended to save api key?
            genai.configure(api_key='AIzaSyDZ-DCljJFFfiKF7gKJIZIvOQg4NijXY4k')
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = f'Summarize the book {bookName} by {authorName} in 5 sentences or less.'
            response = model.generate_content(prompt)
            summary = response.text
            return summary 
        except Exception as error:
            # TODO: Handle exception
            print(error)
            pass
        
        # TODO: Change the empty return. Maybe the return should be at the end of the function
        return ""
        
            


    