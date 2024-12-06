from .GoogleBook import GoogleBook


def parse_book_info(book_info: dict) -> GoogleBook:
    """
    Parse the book information returned by the Google Books API.
    """
    volume_info = book_info.get("volumeInfo", {})
    title = volume_info.get("title", "")
    google_id = book_info.get("id", "")
    googleBook = GoogleBook(google_id=google_id, title=title)
    return googleBook
