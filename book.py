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
        return f"Book({self.id!r}, {self.title!r}, {self.author!r}, {self.status!r})"

    # Turns a Book object to a dict 
    def to_dict(self):
        return self.__dict__

    # Takes a saved dictionary fro json file and rebuilds a Book object
    @staticmethod
    def from_dict(data):
        return Book(**data)  #unpacking the dictionary
