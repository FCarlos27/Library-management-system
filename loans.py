from database import connect_database
from tkinter import messagebox, ttk
from tkinter import *
from books import search_book, decrease_book_quantity, increase_book_quantity, create_book_treeview
from students import search_student, student_form, create_student_treeview
import sqlite3

def loans_form(root):

    loans_frame = Frame(root, bg="white", bd=2, relief=RIDGE)
    loans_frame.place(x=205, y=98, height=585, width=1065)
    header = Label(loans_frame, text="Loans Management", bg="#0B5345", fg="white", font=("times new roman", 15, "bold"), anchor="center")
    header.pack(fill=X)

    backbutton_image = PhotoImage(file="images\\return.png")
    back_button = Button(loans_frame, image=backbutton_image, cursor="hand2", bg="#2b7192",bd=0 , command=lambda: loans_frame.destroy())
    back_button.place(x=5, y=0)

    # Start of left frame
    left_frame = Frame(loans_frame, bg="white", )
    left_frame.pack(side=LEFT, fill=Y)

    student_id_label = Label(left_frame, text="Student ID", bg="white", font=("times new roman", 12))
    student_id_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    student_id_entry = Entry(left_frame, font=("times new roman", 12), bd=2, relief=GROOVE)
    student_id_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    book_name_label = Label(left_frame, text="Book Name", bg="white", font=("times new roman", 12))
    book_name_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    book_name_entry = Entry(left_frame, font=("times new roman", 12), bd=2, relief=GROOVE)
    book_name_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    loan_date_label = Label(left_frame, text="Loan Date", bg="white", font=("times new roman", 12))
    loan_date_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    loan_date_entry = Entry(left_frame, font=("times new roman", 12), bd=2, relief=GROOVE)
    loan_date_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    return_date_label = Label(left_frame, text="Return Date", bg="white", font=("times new roman", 12))
    return_date_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
    return_date_entry = Entry(left_frame, font=("times new roman", 12), bd=2, relief=GROOVE)
    return_date_entry.grid(row=3, column=1, padx=10, pady=10)
    # End of left frame

    # Start of right frame
    right_frame = Frame(loans_frame, bg="white")
    right_frame.pack(side=RIGHT, fill=BOTH, expand=1)

    student_frame = Frame(right_frame, bg="blue")
    student_frame.pack(fill=BOTH, expand=1)

    student_treeview = create_student_treeview(student_frame)
    student_treeview.pack(fill=X, expand=1, anchor="s")

    book_frame = Frame(right_frame, bg="red")
    book_frame.pack(fill=BOTH, expand=1, pady=10)

    book_treeview = create_book_treeview(book_frame)
    book_treeview.pack(fill=X, expand=1, anchor="s")
    # End of right frame
    

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
