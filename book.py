"""
Represents what a book is.
Handles converting to/from a dictionary for JSON storage.
"""


class Book:
    def __init__(
            self,
            title,
            author,
            status = "to_read",
            rating = None,
            notes = None,
            id = None
    ):
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
