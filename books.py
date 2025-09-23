from database import get_connection
from datetime import datetime, timedelta
import sqlite3

def add_book(title, author, quantity):
    # Adds a new book to BOOKS table or increases quantity if it already exists
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # If book exists, update quantity
        if search_book(title):
            increase_book_quantity(title, quantity)
            return "updated"

        # Book doesn't exist, insert new record
        cursor.execute("INSERT INTO BOOKS (title, author, quantity) VALUES (?, ?, ?)",
            (title.strip(), author.strip(), quantity)
        )
        conn.commit()
        return "added"

    except Exception as e:
        return f"error: {str(e)}"

    finally:
        conn.close()
    
def view_books():
    # Display all books in the database with quantity > 0
    try:
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM BOOKS')
        books = [dict(row) for row in cursor.fetchall()]
        return [book for book in books if book['quantity'] > 0] or None
    except Exception as e:
        return f"error: {str(e)}"
    finally:
        conn.close()

 
def search_book(book_name):
    # Search for a book by title
    try: 
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM BOOKS WHERE title = ?', (book_name,))
        result = cursor.fetchone()
        return dict(result) if result else None
    except Exception as e:
        return f"error: {str(e)}"
    finally:
        conn.close()
    
def search_book_by_id(book_id):
    # Search for a book by ID
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM BOOKS WHERE id = ?', (book_id,))
    result = cursor.fetchone()
    conn.close()

    return dict(result) if result else None
    
def increase_book_quantity(book_name, quantity=1):
    if search_book(book_name) is None:
        return "Book not found."
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT quantity FROM BOOKS WHERE title = ?', (book_name,))
        result = cursor.fetchone()

        new_quantity = result[0] + quantity
        cursor.execute('UPDATE BOOKS SET quantity = ? WHERE title = ?', (new_quantity, book_name))
        conn.commit()
        return new_quantity
    except Exception as e:
        return f"error: {str(e)}"
    finally:
        conn.close()

    
def decrease_book_quantity(book_name):
    if search_book(book_name) is None:
        return "Book not found."
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT quantity FROM BOOKS WHERE title = ?', (book_name,))
        result = cursor.fetchone()

        if result and result[0] > 0:
            new_quantity = result[0] - 1
            cursor.execute('UPDATE BOOKS SET quantity = ? WHERE title = ?', (new_quantity, book_name))
            conn.commit()
            return new_quantity
        else:
            return 0
    except Exception as e:
        return f"error: {str(e)}"
    finally:
        conn.close()


