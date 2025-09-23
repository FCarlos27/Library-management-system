import tkinter as tk
from tkinter import *
from datetime import datetime, timedelta
from tkinter import messagebox, ttk
from students import add_student
from books import add_book
from loans import borrow_book, return_book
from penalties import add_penalty
from database import initialize_database

initialize_database()

def launch_gui():
    root = tk.Tk()
    root.title("Library Management System")
    root.geometry("1200x800")

    style = ttk.Style()
    style.theme_use("default")

    # Tab styling
    style.configure("TNotebook.Tab", background="#dbeafe", foreground="#1e3a8a",
                    font=("Helvetica", 11, "bold"), padding=[10, 5])
    style.map("TNotebook.Tab", background=[("selected", "#93c5fd")])

    # Frame styling
    style.configure("Custom.TFrame", background="#f0f9ff")

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")

    # Create and style tabs
    tab_students = ttk.Frame(notebook, style="Custom.TFrame")
    tab_books = ttk.Frame(notebook, style="Custom.TFrame")

    notebook.add(tab_students, text="Add Student")
    notebook.add(tab_books, text="Add Book")

    # Build forms inside each tab
    build_add_student(tab_students)
    build_add_book_form(tab_books)
    build_borrow_book_form(tab_books)
    build_return_book_form(tab_books)
    build_penalty_form(tab_students)

    root.mainloop()


def build_add_student(root):
    frame = tk.Frame(root)
    frame.pack(pady=20)

    tk.Label(frame, text="Student ID").grid(row=0, column=0)
    entry_id = tk.Entry(frame)
    entry_id.grid(row=0, column=1)

    tk.Label(frame, text="Name").grid(row=1, column=0)
    entry_name = tk.Entry(frame)
    entry_name.grid(row=1, column=1)

    tk.Label(frame, text="Age").grid(row=2, column=0)
    entry_age = tk.Entry(frame)
    entry_age.grid(row=2, column=1)

    tk.Label(frame, text="Phone").grid(row=3, column=0)
    entry_phone = tk.Entry(frame)
    entry_phone.grid(row=3, column=1)

    def handle_add():
        try:
            id = int(entry_id.get())
            name = entry_name.get().strip()
            age = int(entry_age.get())
            phone = entry_phone.get().strip()
            result = add_student(id, name, age, phone)
            if result == "success":
                messagebox.showinfo("Success", "Student added.")
            elif result == "exists":
                messagebox.showwarning("Duplicate", "Student ID already exists.")
            else:
                messagebox.showerror("Error", result)
        except ValueError:
            messagebox.showwarning("Invalid Input", "ID and Age must be numbers.")

    tk.Button(frame, text="Add Student", command=handle_add, width=20, height=2, font=("Arial", 12)).grid(row=4, columnspan=2, pady=10)

def build_add_book_form(root):
    frame = tk.Frame(root)
    frame.pack(pady=20)

    # Title
    tk.Label(frame, text="Book Title:").grid(row=0, column=0, sticky="e")
    entry_title = tk.Entry(frame, width=40)
    entry_title.grid(row=0, column=1)

    # Author
    tk.Label(frame, text="Author:").grid(row=1, column=0, sticky="e")
    entry_author = tk.Entry(frame, width=40)
    entry_author.grid(row=1, column=1)

    # Quantity
    tk.Label(frame, text="Quantity:").grid(row=2, column=0, sticky="e")
    entry_quantity = tk.Entry(frame, width=40)
    entry_quantity.grid(row=2, column=1)

    # Button
    def handle_add_book():
        title = entry_title.get().strip()
        author = entry_author.get().strip()
        try:
            quantity = int(entry_quantity.get())
        except ValueError:
            messagebox.showwarning("Invalid Input", "Quantity must be a number.")
            return

        result = add_book(title, author, quantity)
        if result == "added":
            messagebox.showinfo("Success", "Book added successfully.")
        elif result == "updated":
            messagebox.showinfo("Updated", "Book already exists. Quantity increased.")
        else:
            messagebox.showerror("Error", result)

        # Clear fields
        entry_title.delete(0, tk.END)
        entry_author.delete(0, tk.END)
        entry_quantity.delete(0, tk.END)

    tk.Button(frame, text="Add Book", command=handle_add_book, width=20, height=2, font=("Arial", 12)).grid(row=3, columnspan=2, pady=15)

def build_borrow_book_form(root):
    frame = tk.Frame(root)
    frame.pack(pady=20)

    # Student ID
    tk.Label(frame, text="Student ID:").grid(row=0, column=0, sticky="e")
    entry_student_id = tk.Entry(frame, width=40)
    entry_student_id.grid(row=0, column=1)

    # Book Title
    tk.Label(frame, text="Book Title:").grid(row=1, column=0, sticky="e")
    entry_book_title = tk.Entry(frame, width=40)
    entry_book_title.grid(row=1, column=1)

    # Loan Date
    today = datetime.now().strftime("%Y-%m-%d") # Default to today's date
    tk.Label(frame, text=f"Loan Date (YYYY-MM-DD):").grid(row=2, column=0, sticky="e")
    entry_loan_date = tk.Entry(frame, width=40)
    entry_loan_date.grid(row=2, column=1)
    entry_loan_date.insert(0, today)

    # Return Date
    tk.Label(frame, text="Return Date (YYYY-MM-DD):").grid(row=3, column=0, sticky="e")
    entry_return_date = tk.Entry(frame, width=40)
    entry_return_date.grid(row=3, column=1)
    entry_return_date.insert(0, (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")) # Default return date 30 days later

    # Button
    def handle_borrow_book():
        try:
            student_id = int(entry_student_id.get())
            book_title = entry_book_title.get().strip()
            loan_date = entry_loan_date.get().strip()
            return_date = entry_return_date.get().strip()
            # Validate date format
            try:
                datetime.strptime(loan_date, "%Y-%m-%d")
                datetime.strptime(return_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning("Invalid Input", "Loan dates must be in YYYY-MM-DD format.")
                return
            result = borrow_book(student_id, book_title, loan_date, return_date)
            if result == "Loan recorded successfully.":
                messagebox.showinfo("Success", result)
            else:
                messagebox.showerror("Error", result)
        except ValueError:
            messagebox.showwarning("Invalid Input", "Student ID must be a number.")

        # Clear fields
        entry_student_id.delete(0, tk.END)
        entry_book_title.delete(0, tk.END)
        entry_loan_date.delete(0, tk.END)
        entry_return_date.delete(0, tk.END)

    tk.Button(frame, text="Borrow Book", command=handle_borrow_book, width=20, height=2, font=("Arial", 12)).grid(row=4, columnspan=2, pady=15)

def build_return_book_form(root):
    frame = tk.Frame(root)
    frame.pack(pady=20)

    # Student ID
    tk.Label(frame, text="Student ID:").grid(row=0, column=0, sticky="e")
    entry_student_id = tk.Entry(frame, width=40)
    entry_student_id.grid(row=0, column=1)

    # Book Title
    tk.Label(frame, text="Book Title:").grid(row=1, column=0, sticky="e")
    entry_book_title = tk.Entry(frame, width=40)
    entry_book_title.grid(row=1, column=1)

    # Button
    def handle_return_book():
        try:
            student_id = int(entry_student_id.get())
            book_title = entry_book_title.get().strip()
            result = return_book(student_id, book_title)
            if result == "Book returned. Loan status updated":
                messagebox.showinfo("Success", result)
            else:
                messagebox.showerror("Error", result)
        except ValueError:
            messagebox.showwarning("Invalid Input", "Student ID must be a number.")

        # Clear fields
        entry_student_id.delete(0, tk.END)
        entry_book_title.delete(0, tk.END)

    tk.Button(frame, text="Return Book", command=handle_return_book, width=20, height=2, font=("Arial", 12)).grid(row=2, columnspan=2, pady=15)

def build_penalty_form(root):
    frame = tk.Frame(root)
    frame.pack(pady=20)

    # Student ID
    tk.Label(frame, text="Student ID:").grid(row=0, column=0, sticky="e")
    entry_student_id = tk.Entry(frame, width=40)
    entry_student_id.grid(row=0, column=1)

    # Amount
    tk.Label(frame, text="Penalty Amount:").grid(row=1, column=0, sticky="e")
    entry_amount = tk.Entry(frame, width=40)
    entry_amount.grid(row=1, column=1)

    # Reason
    tk.Label(frame, text="Reason:").grid(row=2, column=0, sticky="e")
    entry_reason = tk.Entry(frame, width=40)
    entry_reason.grid(row=2, column=1)

    # Button
    def handle_add_penalty():
        try:
            student_id = int(entry_student_id.get())
            amount = float(entry_amount.get())
            reason = entry_reason.get().strip()
            result = add_penalty(student_id, amount, reason)
            if result == "success":
                messagebox.showinfo("Success", "Penalty added successfully.")
            elif result == "student_not_found":
                messagebox.showwarning("Not Found", "Student ID does not exist.")
            else:
                messagebox.showerror("Error", result)
        except ValueError:
            messagebox.showwarning("Invalid Input", "Student ID must be a number and Amount must be a valid number.")

        # Clear fields
        entry_student_id.delete(0, tk.END)
        entry_amount.delete(0, tk.END)
        entry_reason.delete(0, tk.END)

    tk.Button(frame, text="Add Penalty", command=handle_add_penalty, width=20, height=2, font=("Arial", 12)).grid(row=3, columnspan=2, pady=15)

if __name__ == "__main__":
    launch_gui()
