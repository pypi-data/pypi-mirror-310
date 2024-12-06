from .GoogleBook import GoogleBook
from .utils import parse_book_info


class GoogleBookSearchResult:

    def __init__(self, api_result: str):
        self.api_result = api_result
        self.books_result = self.parse_book_info()

    def parse_book_info(self) -> list[GoogleBook]:
        if not "items" in self.api_result:
            return []
        books = []
        for item in self.api_result["items"]:
            books.append(parse_book_info(item))        
        return books
    

    def get_books(self) -> list[GoogleBook]:
        return self.books_result
