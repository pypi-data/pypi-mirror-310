import requests
from .GoogleBook import GoogleBook
from .GoogleBookSearchResult import GoogleBookSearchResult


class GoogleBooksAPI:
    def __init__(self, api_base_url: str, http_client:requests):
        self.api_base_url = api_base_url
        self.http_client = http_client

    def search_book_by_title(self, title: str) -> list[GoogleBook]:
        if not title.strip():
            raise ValueError("Title cannot be empty.")
        params = {"q": f"{title}+inauthor"}
        try:
            response = self.http_client.get(f"{self.api_base_url}volumes", params=params)
            response.raise_for_status()
            googleBookSearchResult = GoogleBookSearchResult(response.json())
            return googleBookSearchResult.get_books()
        except requests.exceptions.RequestException as e:
            raise ValueError(f"API request failed: {e}")
        except ValueError as e:
            raise ValueError(f"Invalid JSON response: {e}")
