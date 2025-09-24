from database import connect_database
import pymysql

def add_book(title, author, quantity, year, edition="", language=""):
    # Adds a new book to BOOKS table or increases quantity if it already exists
    conn, cursor = connect_database()
    try:
        # If book exists, update quantity
        if search_book(title):
            increase_book_quantity(title, quantity)
            return "updated"

        # Book doesn't exist, insert new record
        cursor.execute("INSERT INTO BOOKS (title, author, quantity, year, edition, language) VALUES (%s, %s, %s, %s, %s, %s)",
            (title.strip(), author.strip(), quantity, year, edition.strip(), language.strip())
        )
        conn.commit()
        return True

    except Exception as e:
        return e

    finally:
        conn.close()
    
def view_books():
    # Display all books in the database with quantity > 0
    conn, cursor = connect_database()
    try:
        cursor.execute('SELECT * FROM BOOKS')
        books = [dict(row) for row in cursor.fetchall()]
        return [book for book in books if book['quantity'] > 0] or None
    except Exception as e:
        return f"error: {str(e)}"
    finally:
        conn.close()

 
def search_book(title):
    conn, cursor = connect_database()
    try:
        query = "SELECT * FROM BOOKS WHERE title = %s"
        cursor.execute(query, (title,))
        result = cursor.fetchone()
        return dict(result) if result else None
    except Exception: 
        return False
    finally:
        if conn:
            conn.close()
    
def increase_book_quantity(title, quantity=1):
    conn, cursor = connect_database()
    if search_book(title) is None:
        return False

    try:
        query = "SELECT quantity FROM BOOKS WHERE title = %s"
        cursor.execute(query, (title,))
        result = cursor.fetchone()

        new_quantity = result['quantity'] + quantity
        query = 'UPDATE BOOKS SET quantity = %s WHERE title = %s'
        cursor.execute(query, (new_quantity, title))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        if conn:
            conn.close()
            

    
def decrease_book_quantity(title):
    if search_book(title) is None:
        return "Book not found."
    
    conn, cursor = connect_database()
    try:
        cursor.execute('SELECT quantity FROM BOOKS WHERE title = %s', (title,))
        result = cursor.fetchone()

        if result and result["quantity"] > 0:
            new_quantity = result["quantity"] - 1
            cursor.execute('UPDATE BOOKS SET quantity = %s WHERE title = %s', (new_quantity, title))
            conn.commit()
            return new_quantity
        else:
            return 0
    except Exception as e:
        return f"error: {str(e)}"
    finally:
        conn.close()

print(decrease_book_quantity("Test Book"))
