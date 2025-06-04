"""Defines commands that can be used in the terminal"""


import typer
import uuid
from typing import Optional
from book import Book
from storage import load_books, save_books
from metadata import MetadataFetcher

app = typer.Typer()

def show_error(message: str):
    """Display error message with red 'Error:' prefix"""
    typer.secho("Error: ", fg="red", bold=True, nl=False, err=True)
    typer.echo(message, err=True)

def show_success(message: str):
    """Display success message with green checkmark"""
    typer.secho("✓ ", fg="green", bold=True, nl=False)
    typer.echo(message)

def show_info(message: str):
    """Display info message with blue info icon"""
    typer.secho("ℹ ", fg="blue", bold=True, nl=False)
    typer.echo(message)

def _find_book_by_id(book_id: str) -> tuple[Book, list[Book]]:
    """Returns (found book, all_books)"""
    books = load_books()
    matching_book = [b for b in books if b.id.startswith(book_id)]

    if not matching_book:
        typer.echo(f"No book found with ID starting with '{book_id}'", err=True)
        raise typer.Exit(1)
    if len(matching_book) > 1:
        typer.echo(f"Multiple books match '{book_id}'. Use more characters", err=True)
        for book in matching_book:
            typer.echo(f"- Full ID: {book.short_id}: {book.title}", err=True)
        raise typer.Exit(1)

    return matching_book[0], books

def _display_book_details(book: Book, show_full_id: bool = False):
    """Display formatted book details"""
    book_id = book.id if show_full_id else book.short_id
    
    typer.secho(f"[{book_id}] ", fg="cyan", bold=True, nl=False)
    typer.secho(f"{book.title}", fg="white", bold=True, nl=False)
    typer.echo(f" by {book.author}")
    
    status_color = {
        "to_read": "yellow",
        "reading": "blue", 
        "read": "green",
        "did_not_finish": "red"
    }.get(book.status, "white")
    
    typer.secho(f"  Status: ", nl=False)
    typer.secho(f"{book.status.replace('_', ' ').title()}", fg=status_color, nl=False)
    
    if book.rating:
        typer.echo(f" | Rating: {'⭐' * book.rating} ({book.rating}/5)")
    else:
        typer.echo()
    
    if book.year:
        typer.echo(f"  Published: {book.year}")
    if book.publisher:
        typer.echo(f"  Publisher: {book.publisher}")
    if book.page_count:
        typer.echo(f"  Pages: {book.page_count}")
    if book.isbn:
        typer.echo(f"  ISBN: {book.isbn}")
    if book.notes:
        typer.echo(f"  Notes: {book.notes}")
    if book.description and book.description != "No description available":
        desc = book.description[:200] + "..." if len(book.description) > 200 else book.description
        typer.echo(f"  Description: {desc}")

@app.command()
def add(
    title: str = typer.Argument(..., help="Title of the book"),
    author: str = typer.Argument(..., help="Author of the book"),
    status: str = typer.Option(
        "to_read",
        help="Reading status (to_read/reading/read/did_not_finish)",
        case_sensitive=False,
        autocompletion=lambda:["to_read", "reading", "read", "did_not_finish"]
    ),
    rating: Optional[int] = typer.Option(None, help="Rating (1-5)"),
    notes: Optional[str] = typer.Option(None, help="Additional notes"),
    no_metadata: bool = typer.Option(False, "--no-metadata", help="Skip metadata fetching")
):
    """Add a new book to the tracker with automatic metadata fetching"""
    try:
        books = load_books()

        new_book = Book(
            title = title,
            author = author,
            status = status,
            rating = rating,
            notes = notes,
            id = str(uuid.uuid4())
        )

        if not no_metadata:
            show_info(f"Fetching metadata for '{title}' by {author}...")
            metadata = MetadataFetcher.fetch_metadata(title, author)

            if metadata:
                new_book.title = metadata.get("title", title)
                new_book.author = metadata.get("author", author)
                new_book.year = metadata.get("year")
                new_book.isbn = metadata.get("isbn")
                new_book.publisher = metadata.get("publisher")
                new_book.page_count = metadata.get("page_count")
                new_book.description = metadata.get("description")
                new_book.olid = metadata.get("olid")

                show_success("Metadata fetched successfully!")
            else:
                show_info("No metadata found")

        books.append(new_book)
        save_books(books)

        typer.echo()
        show_success(f"Added book to your library:")
        _display_book_details(new_book)

    except ValueError as e:
        show_error(str(e))
        raise typer.Exit(1)
    except Exception as e:
        show_error(f"An unexpected error ocurred: {str(e)}")
        raise typer.Exit(1)

@app.command()
def list(
        status: Optional[str] = typer.Option(None, help="Filter by status"),
        author: Optional[str] = typer.Option(None, help="Filter by author"),
        detailed: bool = typer.Option(False, "--detailed", "-d", help="Show detailed information")
):
    """List all books, optionally filtered by status"""
    books = load_books()

    #Filters
    if status:
        books = [b for b in books if b.status == status.lower()]
    if author:
        books = [b for b in books if b.author == author.lower()]
    if not books:
        typer.echo("No books found")
        return

    #Sort by title
    books.sort(key=lambda x: x.title.lower())
    
    typer.echo(f"\nFound {len(books)} book(s):")

    for book in books:
        if detailed:
            _display_book_details(book)
            typer.echo()
        else:
            rating_str = f" ({'⭐' * book.rating})" if book.rating else ""
            year_str = f" ({book.year})" if book.year else ""
            typer.secho(f"[{book.short_id}] ", fg="cyan", nl=False)
            typer.echo(f"{book.title} by {book.author}{year_str} - {book.status.replace('_', ' ').title()}{rating_str}")

@app.command()
def update(
    book_id: str = typer.Argument(..., help="ID or beginninig of ID of the book to update"),
    status: str = typer.Option(None, help="New status (to_read/reading/read/did_not_finish)"),
    rating: int = typer.Option(None, help="New rating (1-5)"),
    notes: str = typer.Option(None, help="New notes")
):
    """Update a book's details by it's ID or partial ID"""
    try:
        book, books = _find_book_by_id(book_id)
        
        updated_fields = []
        if status:
            old_status = book.status
            book.status = status.lower()
            updated_fields.append(f"status: {old_status} → {book.status}")
        if rating is not None:
            old_rating = book.rating
            book.rating = rating
            updated_fields.append(f"rating: {old_rating or 'None'} → {rating}")
        if notes is not None:
            book.notes = notes
            updated_fields.append("notes updated")

        save_books(books)

        if updated_fields:
            show_success(f"Book updated ({', '.join(updated_fields)}):")
            _display_book_details(book)
        else:
            show_info("No changes made to the book")
    except ValueError as e:
        show_error(str(e))
        raise typer.Exit(1)

@app.command()
def show(book_id: str = typer.Argument(..., help="ID or beginning of ID of the book to show")):
    """Show detailed information about a specific book"""
    book, _ = _find_book_by_id(book_id)
    
    typer.echo("\nBook Details:")
    typer.echo("=" * 50)
    _display_book_details(book, show_full_id=True)

@app.command()
def delete(book_id: str = typer.Argument(..., help="ID or beginning of ID of the book to delete")):
    """Delete a book by its ID or partial ID"""
    book, books = _find_book_by_id(book_id)

    #Confirmation
    if not typer.confirm(f"Are you sure you want to delete '{book.title}' by {book.author}?"):
        show_info("Deletion cancelled")
        return 

    books.remove(book)
    save_books(books)
    show_success(f"Book deleted: {book.title} by {book.author}")
