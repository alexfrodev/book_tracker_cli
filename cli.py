"""Defines commands that can be used in the terminal"""


import typer
import uuid
from typing import Optional
from book import Book
from storage import load_books, save_books

app = typer.Typer()

def show_error(message: str):
    """Display errpr message with red 'Error:' prefix"""
    typer.secho("Error: ", fg="red", bold=True, nl=False, err=True)
    typer.echo(message, err=True)

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
            typer.echo(f"- Full ID: {book.id}", err=True)
        raise typer.Exit(1)

    return matching_book[0], books

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
    notes: Optional[str] = typer.Option(None, help="Additional notes")
):
    """Add a new book to the tracker"""
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

        books.append(new_book)
        save_books(books)
        typer.echo(f"Added: {new_book.title} by {new_book.author}")

    except ValueError as e:
        show_error(str(e))
        raise typer.Exit(1)
    except Exception as e:
        show_error("An unexpected error occurred")
        raise typer.Exit(1)

@app.command()
def list(status: str = typer.Option(None, help="Filter by status")):
    """List all books, optionally filtered by status"""
    books = load_books()
    if status:
        books = [b for b in books if b.status == status]
    if not books:
        typer.echo("No books found")
        return
    for book in books:
        typer.echo(f"[{book.short_id}] {book.title} by {book.author} ({book.status})")

@app.command()
def update(
    book_id: str = typer.Argument(..., help="ID or beginninig of ID of the book to update"),
    status: str = typer.Option(None, help="New status (to_read/reading/read/did_not_finish)"),
    rating: int = typer.Option(None, help="New rating (1-5)"),
    notes: str = typer.Option(None, help="New notes")
):
    """Update a book's details by it's ID or partial ID"""
    book, books = _find_book_by_id(book_id)
    if book:
        if status:
            book.status = status
        if rating is not None:
            book.rating = rating
        if notes is not None:
            book.notes = notes
        save_books(books)
        typer.echo(f"Book updated: [{book.short_id}] {book.title} by {book.author} ({book.status})")
        return
    typer.echo(f"Book with ID {book_id} not found", err=True)
    raise typer.Exit(1)

@app.command()
def delete(book_id: str = typer.Argument(..., help="ID or beginning of ID of the book to delete")):
    """Delete a book by its ID or partial ID"""
    book, books = _find_book_by_id(book_id)
    original_count = len(books)
    books.remove(book)

    if len(books) == original_count:
        typer.echo(f"Book with ID {book_id} not found", err=True)
        raise typer.Exit(1)

    save_books(books)
    typer.echo(f"Book deleted: [{book_id}] {book.title} by {book.author}")
