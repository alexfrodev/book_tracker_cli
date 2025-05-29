"""
Represents what a book is.
Handles converting to/from a dictionary for JSON storage.
"""

from typing import Optional

class Book:
    VALID_STATUSES = {"to_read", "reading", "read", "did_not_finish"}

    def __init__(
            self,
            title: str,
            author: str,
            status: str = "to_read",
            rating: Optional[int] = None,
            notes: Optional[str] = None,
            id: Optional[str] = None
    ):
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")
        if not author or not author.strip():
            raise ValueError("Author cannot be empty")

        status = status.lower().strip()
        if status not in self.VALID_STATUSES:
            valid_statuses = ", ".join(sorted(self.VALID_STATUSES))
            raise ValueError(f"Invalid status. Must be one of: {valid_statuses}")
        if rating is not None and (rating < 1 or rating > 5):
            raise ValueError("Rating must be between 1 and 5")

        self.title = title
        self.author = author
        self.status = status
        self.rating = rating
        self.notes = notes
        self.id = id


    def __repr__(self):
        return f"({self.id!r}: {self.title!r} by {self.author!r} - {self.status!r})"

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
        return self.id[:8]
