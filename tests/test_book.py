import unittest
from book import Book

class TestBook(unittest.TestCase):

    def test_to_dict_and_from_dict(self):
        original = Book(
            id="123",
            title="Clean Code",
            author="Robert C. Martin",
            status="to_read",
            rating=5,
            notes="Great book"
        )
        data = original.to_dict()
        reconstructed = Book.from_dict(data)

        self.assertEqual(reconstructed.id, original.id)
        self.assertEqual(reconstructed.title, original.title)
        self.assertEqual(reconstructed.author, original.author)
        self.assertEqual(reconstructed.status, original.status)
        self.assertEqual(reconstructed.rating, original.rating)
        self.assertEqual(reconstructed.notes, original.notes)

if __name__ == '__main__':
    unittest.main()

