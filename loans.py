from database import get_connection
from books import search_book, decrease_book_quantity, increase_book_quantity
from students import search_student
import sqlite3

def borrow_book(student_id, book_name, loan_date, return_date, status='active'):
    # Adds a new loan to LOANS table and decreases book quantity.
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Check if book is available and student exists
        if search_student(student_id) is None:
            return "Student not found."
        if search_book(book_name) is None or search_book(book_name)['quantity'] == 0:
            return "Book not available."
        
        cursor.execute("INSERT INTO LOANS (student_id, book_name, loan_date, return_date, status) VALUES (?, ?, ?, ?, ?)",
                       (student_id, book_name, loan_date, return_date, status))
        conn.commit()
        decrease_book_quantity(book_name)
        return "Loan recorded successfully."
    except Exception as e:
        return f"error: {str(e)}"
    finally:
        conn.close()

def return_book(student_id, book_name):
    # Modifies the LOANS table to mark a book as returned and increases book quantity.
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Check if loan record exists
        if search_loan(student_id, book_name) is None:
            return "No loan record found for this student and book."
        
        cursor.execute('UPDATE LOANS SET status = "returned" WHERE student_id = ? AND book_name = ?', 
                     (student_id, book_name))
        conn.commit()
        increase_book_quantity(book_name)
        return "Book returned. Loan status updated"
    except Exception as e:
        return f"error: {str(e)}"
    finally:
        conn.close()    

def search_loan(student_id, book_name, loan_date=None):
    try:
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        if loan_date:
            cursor.execute('SELECT * FROM LOANS WHERE student_id = ? AND book_name = ? AND loan_date = ?', (student_id, book_name, loan_date))
            result = cursor.fetchone()
            return dict(result) if result else None
        cursor.execute('SELECT * FROM LOANS WHERE student_id = ? AND book_name = ?', (student_id, book_name))
        result = cursor.fetchall()
        return dict(result) if result else None
    except Exception as e:
        return f"error: {str(e)}"
    finally:
        conn.close()
