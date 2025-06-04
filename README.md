# Book Tracker CLI

A terminal-based application to track books you've read, want to read, or are currently reading. Features automatic metadata fetching from Open Library API with local caching for improved performance.

## Features

- ✅ Add books with automatic metadata fetching (title, author, year, ISBN, publisher, page count, description)
- 📖 Track reading status (to read, reading, read, did not finish)
- ⭐ Rate books (1-5 stars)
- 📝 Add personal notes to books
- 🔍 List and filter books by status or author
- 🆔 Unique ID system for easy book management
- 💾 Local JSON storage with metadata caching
- 🎨 Colorful terminal output with intuitive formatting

## Installation

1. Clone the repository:
```bash
git clone https://github.com/alexfrodev/book_tracker_cli.git
cd book_tracker_cli
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py --help
```

## Usage

### Adding Books

Add a new book with automatic metadata fetching:
```bash
python main.py add "The Great Gatsby" "F. Scott Fitzgerald"
```

Add a book with custom status and rating:
```bash
python main.py add "1984" "George Orwell" --status reading --rating 5
```

Add a book with notes:
```bash
python main.py add "Dune" "Frank Herbert" --notes "Epic sci-fi masterpiece"
```

Skip metadata fetching (faster, but less information):
```bash
python main.py add "Some Book" "Some Author" --no-metadata
```

### Listing Books

List all books:
```bash
python main.py list
```

Filter by reading status:
```bash
python main.py list --status read
python main.py list --status reading
python main.py list --status to_read
python main.py list --status did_not_finish
```

Filter by author:
```bash
python main.py list --author "Stephen King"
```

Show detailed information:
```bash
python main.py list --detailed
```

### Viewing Book Details

Show detailed information for a specific book using its ID:
```bash
python main.py show abc12345
```

You only need the first few characters of the book ID (shown in square brackets when listing books).

### Updating Books

Update a book's reading status:
```bash
python main.py update abc12345 --status read
```

Add or update rating:
```bash
python main.py update abc12345 --rating 4
```

Add or update notes:
```bash
python main.py update abc12345 --notes "Brilliant storytelling"
```

Update multiple fields at once:
```bash
python main.py update abc12345 --status read --rating 5 --notes "Amazing book!"
```

### Deleting Books

Delete a book (with confirmation prompt):
```bash
python main.py delete abc12345
```

## Reading Statuses

The application supports four reading statuses:

- **to_read**: Books you plan to read (default)
- **reading**: Books you're currently reading
- **read**: Books you've finished reading
- **did_not_finish**: Books you started but didn't complete

## Rating System

Books can be rated from 1 to 5 stars:
- ⭐ (1/5) - Poor
- ⭐⭐ (2/5) - Fair
- ⭐⭐⭐ (3/5) - Good
- ⭐⭐⭐⭐ (4/5) - Very Good
- ⭐⭐⭐⭐⭐ (5/5) - Excellent

## Data Storage

- Books are stored in `books.json` in the project directory
- Metadata cache is stored in the `metadata_cache/` directory
- All data is stored locally - no cloud synchronization

## Metadata Fetching

The application automatically fetches book metadata from the [Open Library API](https://openlibrary.org/developers/api), including:

- Verified title and author information
- Publication year
- ISBN
- Publisher
- Page count
- Book description
- Open Library ID

Metadata is cached locally for 24 hours to improve performance and reduce API calls.

## Examples

Here's a typical workflow:

```bash
# Add some books
python main.py add "The Hobbit" "J.R.R. Tolkien" --status to_read
python main.py add "1984" "George Orwell" --status reading
python main.py add "Pride and Prejudice" "Jane Austen" --status read --rating 4

# List all books
python main.py list

# Output:
# Found 3 book(s):
# [a1b2c3d4] 1984 by George Orwell (1949) - Reading
# [e5f6g7h8] Pride and Prejudice by Jane Austen (1813) - Read (⭐⭐⭐⭐)
# [i9j0k1l2] The Hobbit by J.R.R. Tolkien (1937) - To Read

# Update reading progress
python main.py update e5f6 --status read --rating 5 --notes "Timeless classic"

# Show detailed information
python main.py show i9j0

# List only books you've read
python main.py list --status read --detailed
```

## Command Reference

| Command | Description | Options |
|---------|-------------|---------|
| `add` | Add a new book | `--status`, `--rating`, `--notes`, `--no-metadata` |
| `list` | List books | `--status`, `--author`, `--detailed` |
| `show` | Show detailed book information | - |
| `update` | Update book details | `--status`, `--rating`, `--notes` |
| `delete` | Delete a book | - |

## Requirements

- Python 3.7+
- Internet connection (for metadata fetching)

## Dependencies

- `typer` - CLI framework
- `requests` - HTTP library for API calls

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Troubleshooting

**Books not found when using partial IDs**: Use more characters from the book ID to make it unique.

**Metadata fetching fails**: Check your internet connection. The app will still work without metadata, just with less information.

**JSON file corruption**: If `books.json` becomes corrupted, you can delete it to start fresh (you'll lose your book data).

**Permission errors**: Make sure you have write permissions in the directory where you're running the application.
