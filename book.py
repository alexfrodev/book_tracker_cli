"""
Represents what a book is.
Handles converting to/from a dictionary for JSON storage.
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class Book:
    VALID_STATUSES = {"to_read", "reading", "read", "did_not_finish"}

    title: str
    author: str
    status: str = "to_read"
    rating: Optional[int] = None
    notes: Optional[str] = None
    id: Optional[str] = None
    isbn: Optional[str] = None
    year: Optional[int] = None
    publisher: Optional[str] = None
    page_count: Optional[int] = None
    description: Optional[str] = None
    olid: Optional[str] = None

    def __post_init__(self):
        """Input validation after initialization"""
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty")
        if not self.author or not self.author.strip():
            raise ValueError("Author cannot be empty")

        self.status = self.status.lower().strip()
        if self.status not in self.VALID_STATUSES:
            valid_statuses = ", ".join(sorted(self.VALID_STATUSES))
            raise ValueError(f"Invalid status. Must be one of: {valid_statuses}")
        if self.rating is not None and (self.rating < 1 or self.rating > 5):
            raise ValueError("Rating must be between 1 and 5")


    def to_dict(self):
        """Turns a Book object to a dict.""" 
        return self.__dict__

    @staticmethod
    def from_dict(data):
        """Takes a saved dictionary from a json file and rebuilds a Book object"""
        return Book(**data)  #unpacking the dictionary

    @property
    def short_id(self):
        """Return first 8 characters of the ID for display"""
        return self.id[:8] if self.id else None
