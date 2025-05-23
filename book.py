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
