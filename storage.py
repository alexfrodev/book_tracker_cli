""" Utility functions to save and load books from a JSON file."""


import json
from pathlib import Path
from book import Book


BOOKS = Path("books.json")


# Opens the file and converts it into a list of books
def load_books():
    if not BOOKS.exists():
        return []
    with open(BOOKS, "r", encoding="utf-8") as file:
        data = json.load(file)
        return [Book.from_dict(book) for book in data]


# Takes a list of Book objects and writes them as json
def save_books(books):
    with open(BOOKS, "w", encoding="utf-8") as file:
        json.dump([book.to_dict() for book in books], file, indent=4)
