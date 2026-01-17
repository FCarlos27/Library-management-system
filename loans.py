from database import connect_database
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from tkinter import * 
from books import search_book, decrease_book_quantity, increase_book_quantity, create_book_treeview, make_optional, search_book_title_author, make_optional, clear_fields
from books import select_book
from books import treeview_data as book_treeview_data
from students import search_student, create_student_treeview, search_bar, select_student
from students import treeview_data as student_treeview_data
import sqlite3, datetime


def treeview_data(treeview: ttk.Treeview) -> None:
    """
    Populate the given Treeview widget with loan records from the database.
    
    Parameters
    ----------
    treeview : Treeview widget to populate with loan data.
    """
    try:
        conn, cursor = connect_database()
        cursor.execute("""
            SELECT L.id AS loan_id, L.student_id, S.name AS student_name,
                   B.title AS book_name,
                   L.loan_date, L.return_date, L.status
            FROM LOANS L
            JOIN STUDENTS S ON L.student_id = S.id
            JOIN BOOKS B ON L.book_id = B.id
        """)
        results = cursor.fetchall()

        treeview.delete(*treeview.get_children())
        for row in results:
            treeview.insert("", END, iid=row["loan_id"], values=(
                row['student_id'],
                row['student_name'],
                row['book_name'],
                row['loan_date'],
                row['return_date'],
                row['status']
            ))
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))
        return e
    finally:
        if conn:
            conn.close()

def create_loan_treeview(parent_frame: Frame) -> ttk.Treeview:
    """
    Create and configure a Treeview widget for displaying student records.

    Parameters
    ----------
    parent_frame : Frame
        The frame in which to place the Treeview.

    Returns
    -------
    ttk.Treeview
        The configured Treeview widget.
    """
    # Configure the Treeview widget and scrollbar
    
    vertical_scrollbar = Scrollbar(parent_frame, orient=VERTICAL)
    loan_treeview = ttk.Treeview(parent_frame, columns=("student_id", "student_name", "book_name", "loan_date", "return_date", "status"), show="headings", yscrollcommand=vertical_scrollbar)
    
    vertical_scrollbar.pack(side=RIGHT, fill=Y, pady=(10,0))
    vertical_scrollbar.config(command=loan_treeview.yview)
    
    # Define column headers
    
    loan_treeview.heading("student_id", text="Student ID", anchor="w")
    loan_treeview.heading("student_name", text="Student Name", anchor="w")
    loan_treeview.heading("book_name", text="Book Name", anchor="w")
    loan_treeview.heading("loan_date", text="Loan Date", anchor="w")
    loan_treeview.heading("return_date", text="Return Date", anchor="w")
    loan_treeview.heading("status", text="Status", anchor="w")

    # Set column widths

    loan_treeview.column("student_id", width=100, anchor="w")
    loan_treeview.column("student_name", width=150, anchor="w")
    loan_treeview.column("book_name", width=200, anchor="w")
    loan_treeview.column("loan_date", width=120, anchor="w")
    loan_treeview.column("return_date", width=120, anchor="w")
    loan_treeview.column("status", width=100, anchor="w")

    treeview_data(loan_treeview)
    return loan_treeview

def loans_form(root: Tk) -> None:
    """
    Build and display the Loans Management interface inside the given root window.

    This function creates a dedicated frame for managing loan records. It includes:
      - A header with a title and back button.
      - A left frame containing entry fields for loan details:
      - Action buttons to add, update, delete, clear, and view loan records.
      - A right frame (built via `build_right_frame`) that can display either:
          * Student/Book data (default mode), or
          * Loan data (loans mode).

    Parameters
    ----------
    root : Tk
        The main application window where the loans management frame will be placed.
    """

    global backbutton_image, treeviews


    loans_frame = Frame(root, bg="white", bd=2, relief=RIDGE)
    loans_frame.place(x=205, y=98, height=585, width=1065)
    header_frame = Frame(loans_frame, bg="#0B5345")
    header_frame.pack(fill=X)

    header = Label(header_frame, text="Loans Management",
                    bg="#0B5345", fg="white",
                    font=("times new roman", 15, "bold"),
                    anchor="center")
    header.grid(row=0, column=1, sticky="W", padx=350)

    backbutton_image = PhotoImage(file="images\\return.png")
    back_button = Button(header_frame, image=backbutton_image,
                            cursor="hand2", bg="#0B5345", bd=0,
                            command=lambda: loans_frame.destroy())
    back_button.grid(row=0, column=0, padx=5)

    # === Left Frame ===
    left_frame = Frame(loans_frame, bg="white", )
    left_frame.pack(side=LEFT)

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
    loan_date_entry = DateEntry(left_frame, font=("times new roman", 12), bd=2, relief=GROOVE, date_pattern="mm/dd/yyyy", width=16)
    loan_date_entry.grid(row=2, column=1, padx=4, pady=10)

    return_date_label = Label(left_frame, text="Return Date", bg="white", font=("times new roman", 12))
    return_date_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
    return_date_entry = DateEntry(left_frame, font=("times new roman", 12), bd=2, relief=GROOVE, date_pattern="mm/dd/yyyy", width=16)
    return_date_entry.grid(row=3, column=1, padx=4, pady=10)

    status_label = Label(left_frame, text="Loan Status", bg="white", font=("times new roman", 12))
    status_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
    status_combobox = ttk.Combobox(left_frame, values=["active", "returned", "overdue", "lost", "renewed"], 
                                   font=("times new roman", 12), state="readonly", width=16)
    status_combobox.set("active")
    status_combobox.grid(row=4, column=1, padx=(16,0), pady=10, sticky="w")
    
    add_button = Button(left_frame, text="Add", font=("times new roman", 12, "bold"), bg="#0B5345", fg="white", cursor="hand2",
                        width=12, command=lambda: add_loan(*entries[:4], *treeviews))
    add_button.grid(row=5, column=0, columnspan=1, padx=(5,0), pady=20)

    update_button = Button(left_frame, text="Update", font=("times new roman", 12, "bold"), bg="#0B5345", fg="white", cursor="hand2",
                        width=12, command=lambda: update_loan(*entries, treeviews[0]))
    update_button.grid(row=5, column=1, columnspan=1, padx=(5,0),pady=10)
    update_button.config(state=DISABLED)

    delete_button = Button(left_frame, text="Delete", font=("times new roman", 12, "bold"), bg="#0B5345", fg="white", cursor="hand2",
                        width=12, command=lambda: delete_loan(*entries[:-1], treeviews[0]))   
    delete_button.grid(row=6, column=0, columnspan=1, padx=(5,0),pady=10)
    delete_button.config(state=DISABLED)

    clear_button = Button(left_frame, text="Clear", font=("times new roman", 12, "bold"), bg="#0B5345", fg="white", cursor="hand2",
                        width=12, command=lambda: clear_fields(*entries[:-1], treeview1=treeviews[0], treeview2=treeviews[1] if len(treeviews) > 1 else None))
    clear_button.grid(row=6, column=1, columnspan=1, padx=(5,0), pady=10)

    view_loans_button = Button(left_frame, text="View Loans", font=("times new roman", 12, "bold"), bg="#0B5345", fg="white", cursor="hand2",
                        width=15, command=lambda: [clear_fields(*entries[:-1]), build_right_frame(right_container, entries, buttons, destroy=True, mode="loans")])
    view_loans_button.grid(row=7, column=0, columnspan=2, pady=10)

    # === Right Frame ===
    right_container = Frame(loans_frame, bg="white")
    right_container.pack(side=RIGHT, fill=BOTH, expand=1)

    entries = [student_id_entry, book_name_entry, loan_date_entry, return_date_entry, status_combobox]
    buttons = [add_button, update_button, delete_button, clear_button]

    _, treeviews = build_right_frame(right_container, entries, buttons, destroy=False, mode="default")

def add_loan(student_id_entry: Entry, book_name_entry: Entry, loan_date_entry: Entry, 
             return_date_entry: Entry, student_treeview: ttk.Treeview = None, book_treeview: ttk.Treeview = None) -> None:
    """
    Validate input fields and insert a new loan record into the database.
    """
    
    if not student_id_entry.get() or not book_name_entry.get():
        messagebox.showwarning("Warning", "Please fill in all required fields.")
        return
    try:
        conn, cursor = connect_database()

        student_id = student_id_entry.get()
        book_name = book_name_entry.get()
        loan_date = loan_date_entry.get_date()
        return_date = return_date_entry.get_date()

        if search_student(student_id) is None:
            messagebox.showwarning("Warning", "Enter a valid student ID.")
            return
        
        book = search_book(book_name)
        if book is None or book['quantity'] == 0:
            messagebox.showwarning("Warning", "Book not available.")
            return

        book_id = book['id']

        student_id = int(student_id)
        loan_date = loan_date.strftime("%y-%m-%d")
        return_date = return_date.strftime("%y-%m-%d")

        if return_date < loan_date or return_date == loan_date:
            messagebox.showwarning("Warning", "Return date must be after loan date.")
            return

        cursor.execute(
            "INSERT INTO LOANS (student_id, book_id, loan_date, return_date, status) VALUES (%s, %s, %s, %s, %s)",
            (student_id, book_id, loan_date, return_date, "active")
        )
        conn.commit()
        decrease_book_quantity(book_name)
        student_treeview_data(student_treeview)
        book_treeview_data(book_treeview)
        clear_fields(student_id_entry, book_name_entry, loan_date_entry, return_date_entry, 
                     treeview1=student_treeview, treeview2=book_treeview)
        messagebox.showinfo("Success", "Loan recorded successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"error: {str(e)}")
    finally:
        conn.close()

def update_loan(student_id_entry: Entry, book_name_entry: Entry, loan_date_entry: DateEntry, 
    return_date_entry: DateEntry, status_combobox: ttk.Combobox, treeview: ttk.Treeview) -> None:

    """
    Update an existing loan record in the database with new values.
    """
    # Extract values from widgets
    student_id = student_id_entry.get().strip()
    book_name = book_name_entry.get().strip()
    loan_date = loan_date_entry.get_date().strftime("%Y-%m-%d")
    return_date = return_date_entry.get_date().strftime("%Y-%m-%d")
    status = status_combobox.get().strip()

    if not student_id or not book_name:
        messagebox.showwarning("Warning", "Please select a loan from the record.")
        return

    today = datetime.datetime.now().date().strftime("%Y-%m-%d")
    if loan_date > today:
        messagebox.showerror("Invalid Date", "Loan date cannot be in the future.")
        return
    if return_date < loan_date:
        messagebox.showerror("Invalid Date", "Return date cannot be earlier than loan date.")
        return

    confirm = messagebox.askyesno("Confirm Update", "Are you sure you want to update this loan?")
    if not confirm:
        return

    try:
        conn, cursor = connect_database()

        cursor.execute("""
            UPDATE LOANS
            SET loan_date = %s,
                return_date = %s,
                status = %s
            WHERE student_id = %s
              AND book_id = (
                  SELECT b.id
                  FROM BOOKS b
                  WHERE b.title = %s
              )
        """, (loan_date, return_date, status, student_id, book_name))

        conn.commit()
        messagebox.showinfo("Success", "Loan updated successfully.")
        if status.lower() == "returned":
            increase_book_quantity(book_name, "")

        clear_fields(student_id_entry, book_name_entry, loan_date_entry, return_date_entry,
                     treeview1=treeview)
        treeview_data(treeview)

    except Exception as e:
        messagebox.showerror("Error", f"error: {str(e)}")
    finally:
        conn.close()

def delete_loan(student_id_entry: Entry, book_name_entry: Entry, 
                loan_date_entry: DateEntry, return_date_entry: DateEntry, treeview: ttk.Treeview) -> None:
    """
    Delete an existing loan record from the database.
    """

    # Extract values from widgets
    student_id = student_id_entry.get().strip()
    book_name = book_name_entry.get().strip()

    if not messagebox.askyesno("Warning", "Are you sure you want to delete this loan record",  icon='warning'):
        return
    
    if not student_id or not book_name:
        messagebox.showwarning("Warning", "Please select a loan from the record.")
        return
    
    try:
        conn, cursor = connect_database()

        # Check penalties first
        cursor.execute("""
            SELECT COUNT(*) AS cnt
            FROM PENALTIES
            WHERE loan_id = (
                SELECT id FROM LOANS
                WHERE student_id = %s
                AND book_id = (SELECT b.id FROM BOOKS b WHERE b.title = %s)
            )
        """, (student_id, book_name))
        penalty_count = cursor.fetchone()["cnt"]

        if penalty_count > 0:
            messagebox.showwarning("Blocked", "Cannot delete loan: penalties are still linked.")
            return

        # Safe to delete
        cursor.execute("""
            DELETE FROM LOANS
            WHERE student_id = %s
            AND book_id = (SELECT b.id FROM BOOKS b WHERE b.title = %s)
        """, (student_id, book_name))

        conn.commit()
        messagebox.showinfo("Success", "Loan deleted successfully.")

        clear_fields(student_id_entry, book_name_entry, loan_date_entry, return_date_entry,
                    treeview1=treeview)
        treeview_data(treeview)
        # Ask if user wants to increase book quantity
        if messagebox.askyesno("Increase Quantity", "Do you also want to increase the book quantity by 1?"):
            increase_book_quantity(book_name, "")



    except Exception as e:
        conn.rollback()
        messagebox.showerror("Error", f"error: {str(e)}")
    finally:
        conn.close()


def search_loan(search_combobox: str, search_entry: str, treeview: ttk.Treeview) -> list:
    """
    Search for loan records in the database based on a selected criterion.

    This function validates the search input, executes an SQL query against the 
    `LOANS` table (joined with `STUDENTS` and `BOOKS`), and retrieves loan records 
    that match the search criterion provided by the user. The results are displayed 
    in the global `loan_treeview` widget, replacing any existing entries.

    Parameters
    ----------
    search_combobox: The selected search criterion (e.g., "Student ID", "Book Name").
    search_entry : The value entered by the user to filter loan records.

    Returns
    -------
    list
        A list of matching loan records retrieved from the database. Each record 
        is represented as a dictionary-like row object.
    """

    # --- Input Validation ---
    if not search_combobox or not search_entry.strip():
        messagebox.showwarning("Warning", "Please select a search criterion and enter a value.")
        return []

    try:
        conn, cursor = connect_database()
        query = ""
        param = ()

        if search_combobox == "Student ID":
            query = """
                SELECT L.student_id, S.name AS student_name,
                       B.title AS book_name,
                       L.loan_date, L.return_date, L.status
                FROM LOANS L
                JOIN STUDENTS S ON L.student_id = S.id
                JOIN BOOKS B ON L.book_id = B.id
                WHERE L.student_id = %s
            """
            param = (search_entry,)
        elif search_combobox == "Student Name":
            query = """
                SELECT L.student_id, S.name AS student_name,
                       B.title AS book_name,
                       L.loan_date, L.return_date, L.status
                FROM LOANS L
                JOIN STUDENTS S ON L.student_id = S.id
                JOIN BOOKS B ON L.book_id = B.id
                WHERE S.name LIKE %s
            """
            param = (f"%{search_entry}%",)
        elif search_combobox == "Book Name":
            query = """
                SELECT L.student_id, S.name AS student_name,
                       B.title AS book_name,
                       L.loan_date, L.return_date, L.status
                FROM LOANS L
                JOIN STUDENTS S ON L.student_id = S.id
                JOIN BOOKS B ON L.book_id = B.id
                WHERE B.title LIKE %s
            """
            param = (f"%{search_entry}%",)
        elif search_combobox == "Loan Date":
            query = """
                SELECT L.student_id, S.name AS student_name,
                       B.title AS book_name,
                       L.loan_date, L.return_date, L.status
                FROM LOANS L
                JOIN STUDENTS S ON L.student_id = S.id
                JOIN BOOKS B ON L.book_id = B.id
                WHERE L.loan_date = %s
            """
            param = (search_entry,)
        elif search_combobox == "Return Date":
            query = """
                SELECT L.student_id, S.name AS student_name,
                       B.title AS book_name,
                       L.loan_date, L.return_date, L.status
                FROM LOANS L
                JOIN STUDENTS S ON L.student_id = S.id
                JOIN BOOKS B ON L.book_id = B.id
                WHERE L.return_date = %s
            """
            param = (search_entry,)
        elif search_combobox == "Status":
            query = """
                SELECT L.student_id, S.name AS student_name,
                       B.title AS book_name,
                       L.loan_date, L.return_date, L.status
                FROM LOANS L
                JOIN STUDENTS S ON L.student_id = S.id
                JOIN BOOKS B ON L.book_id = B.id
                WHERE L.status = %s
            """
            param = (search_entry,)

        cursor.execute(query, param)
        results = cursor.fetchall()

        treeview.delete(*treeview.get_children())
        for row in results:
            treeview.insert("", END, values=(
                row['student_id'],
                row['student_name'],
                row['book_name'],
                row['loan_date'],
                row['return_date'],
                row['status']
            ))
        return results

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))
        return []
    finally:
        if conn:
            conn.close()

def select_loan(event: Event, student_id_entry: Entry, book_name_entry: Entry, 
                loan_date_entry: Entry, return_date_entry: Entry, status_combobox: Entry, 
                loan_id_entry: Entry=None, treeview: ttk.Treeview = None) -> None:
    """
    Populate loan details into entry fields when a record is selected from the Treeview.

    This function retrieves the currently selected loan record from the global 
    `loan_treeview` widget and fills the corresponding entry fields with its values. 
    It disables editing for certain fields (student ID and book name) to prevent 
    accidental modification. If a `loan_id_entry` widget is provided, the loan ID 
    is also captured and displayed.
    
    Parameters
    ----------
    event : The event object triggered by selecting a Treeview item.
    *entries : Entry widgets to be populated
    treeview: Treeview widget for row selection (focus)
    """

    selected_item = treeview.focus()
    if not selected_item:
        return
    
    # Capture the loan_id from iid
    loan_id = selected_item  

    # Only populate these entries in the penalties form
    if loan_id_entry:
        values = treeview.item(selected_item, 'values')

        student_id_entry.insert(0, values[0])
        student_id_entry.config(state='disabled')

        book_name_entry.insert(0, values[2])
        book_name_entry.config(state='disabled')

        loan_id_entry.insert(0, loan_id)
        loan_id_entry.config(state='disabled')
        return
    
    clear_fields(student_id_entry, book_name_entry, loan_date_entry, return_date_entry)
    values = treeview.item(selected_item, 'values')

    student_id_entry.insert(0, values[0])
    student_id_entry.config(state='disabled')

    book_name_entry.insert(0, values[2])
    book_name_entry.config(state='disabled')

    loan_date_entry.set_date(datetime.datetime.strptime(values[3], "%Y-%m-%d"))
    return_date_entry.set_date(datetime.datetime.strptime(values[4], "%Y-%m-%d"))

    status_combobox.set(values[5])

    
def build_right_frame(parent_frame: Frame, entries: list, buttons: list, destroy: bool=False, mode: str="default"):
    """
    Build the right_frame UI.

    Parameters
    ----------
    parent_frame : The parent container.
    entries : List of entry widgets to be populated.
    buttons: List of button widgets to be configured
    destroy : If True, destroy existing children before rebuilding.
    mode : Determines which UI to build:
        - "default": student/book view
        - "loans": loan view
    """
    global treeviews, back_button_image

    if destroy:
        for widget in parent_frame.winfo_children():
            widget.destroy()

    right_frame = Frame(parent_frame, bg="white")
    right_frame.pack(side=RIGHT, fill=BOTH, expand=1)

    treeviews = []

    if mode == "default":
        # -------------------------------
        # Student + Book section
        # -------------------------------
        student_frame = Frame(right_frame, bg="white")
        student_frame.pack(fill=BOTH, expand=1)

        # Search bar for students
        search_student_frame = Frame(student_frame, bg="white")
        search_student_frame.pack(fill=X, anchor="n")
        search_student_combo = ttk.Combobox(
            search_student_frame,
            values=["Id", "Name"],
            font=("times new roman", 12),
            state="readonly",
            justify=CENTER
        )
        search_student_combo.set("Search By")
        search_student_combo.grid(row=0, column=0, padx=10, pady=5)

        search_student_entry = Entry(search_student_frame, font=("times new roman", 12), bd=2, bg="light gray")
        search_student_entry.grid(row=0, column=1, pady=5)

        search_student_button = Button(
            search_student_frame,
            text="Search",
            font=("times new roman", 12),
            bg="#0B5345", fg="white",
            cursor="hand2", width=10,
            command=lambda: search_bar(search_student_combo.get(), search_student_entry.get(), treeviews[0]))
        search_student_button.grid(row=0, column=2, padx=20, pady=5)

        showall_student_button = Button(
            search_student_frame,
            text="Show All",
            font=("times new roman", 12),
            bg="#0B5345", fg="white",
            cursor="hand2", width=10,
            command=lambda: student_treeview_data(treeviews[0])
        )
        showall_student_button.grid(row=0, column=3, pady=5)

        student_treeview = create_student_treeview(student_frame)
        student_treeview.pack(fill=BOTH, expand=1, anchor="s")
        student_treeview.bind("<ButtonRelease-1>", lambda event: select_student(event, student_treeview, entries[0], None, None, None, None, None))

        # Book section
        book_frame = Frame(right_frame, bg="white")
        book_frame.pack(fill=BOTH, expand=1, pady=10)

        search_book_frame = Frame(book_frame, bg="white")
        search_book_frame.pack(fill=X, anchor="n")
        search_book_combo = ttk.Combobox(
            search_book_frame,
            values=["Title", "Author"],
            font=("times new roman", 12),
            state="readonly",
            justify=CENTER
        )
        search_book_combo.set("Search By")
        search_book_combo.grid(row=0, column=0, padx=10, pady=5)

        search_book_entry = Entry(search_book_frame, font=("times new roman", 12), bd=2, bg="light gray")
        search_book_entry.grid(row=0, column=1, pady=5)

        search_book_button = Button(
            search_book_frame,
            text="Search",
            font=("times new roman", 12),
            bg="#0B5345", fg="white",
            cursor="hand2", width=10,
            command=lambda: search_book_title_author(search_book_combo.get(), search_book_entry.get(), treeviews[1])
        )
        search_book_button.grid(row=0, column=2, padx=20, pady=5)

        showall_book_button = Button(
            search_book_frame,
            text="Show All",
            font=("times new roman", 12),
            bg="#0B5345", fg="white",
            cursor="hand2", width=10,
            command=lambda: book_treeview_data(treeviews[1])
        )
        showall_book_button.grid(row=0, column=3, pady=5)

        buttons[0].config(state=NORMAL)
        buttons[1].config(state=DISABLED)
        buttons[2].config(state=DISABLED)

        book_treeview = create_book_treeview(book_frame)
        book_treeview.pack(fill=X, expand=1, anchor="s")
        book_treeview.bind("<ButtonRelease-1>", lambda event: select_book(event, entries[1], None, None, None, None, None, book_treeview))

        make_optional(search_student_entry)
        make_optional(search_book_entry)

        treeviews.extend([student_treeview, book_treeview])

    elif mode == "loans":
        # -------------------------------
        # Loan section
        # -------------------------------
        search_frame = Frame(right_frame, bg="white")
        search_frame.pack(fill=X, anchor="n", pady=10)

        back_button_image = PhotoImage(file="images\\go-back.png")
        back_button = Button(
            search_frame,
            image=back_button_image,
            cursor="hand2",
            command=lambda: build_right_frame(right_frame, entries, buttons, True, mode="default"),
            bg="white", bd=0
        )
        back_button.grid(row=0, column=0, padx=10, pady=5)

        search_combobox = ttk.Combobox(
            search_frame,
            values=["Student ID", "Student Name", "Book Name", "Loan Date", "Return Date", "Status"],
            font=("times new roman", 12),
            state="readonly",
            justify="center"
        )
        search_combobox.set("Search By")
        search_combobox.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        search_entry_frame = Frame(search_frame, width=180, height=30)
        search_entry_frame.grid(row=0, column=2, pady=5)
        search_entry_frame.grid_propagate(False)

        search_entry = Entry(search_entry_frame, font=("times new roman", 12), bd=2, bg="light gray")
        search_entry.pack(fill="both", expand=True)
        make_optional(search_entry)

        def update_search_entry(event):
            global new_entry
            for widget in search_entry_frame.winfo_children():
                widget.destroy()

            choice = search_combobox.get()
            if choice == "Status":
                new_entry = ttk.Combobox(
                    search_entry_frame,
                    values=["active", "returned", "overdue", "lost", "renewed"],
                    font=("times new roman", 12),
                    state="readonly"
                )
            elif choice in ["Loan Date", "Return Date"]:
                new_entry = DateEntry(
                    search_entry_frame,
                    font=("times new roman", 12),
                    date_pattern="yyyy-mm-dd"
                )
            else:
                new_entry = Entry(search_entry_frame, font=("times new roman", 12), bd=2, bg="light gray")
                make_optional(new_entry)

            new_entry.pack(fill="both", expand=True)

        search_combobox.bind("<<ComboboxSelected>>", update_search_entry)

        search_button = Button(
            search_frame,
            text="Search",
            font=("times new roman", 12),
            bg="#0B5345", fg="white",
            cursor="hand2", width=10,
            command=lambda: search_loan(search_combobox.get(), new_entry.get(), treeviews[0])
        )
        search_button.grid(row=0, column=3, padx=20, pady=5)

        showall_button = Button(
            search_frame,
            text="Show All",
            font=("times new roman", 12),
            bg="#0B5345", fg="white",
            cursor="hand2", width=10,
            command=lambda: treeview_data(treeviews[0])
        )
        showall_button.grid(row=0, column=4, pady=5)

        buttons[0].config(state=DISABLED)
        buttons[1].config(state=NORMAL)
        buttons[2].config(state=NORMAL)

        loan_treeview = create_loan_treeview(right_frame)
        loan_treeview.pack(fill=BOTH, expand=1, anchor="n", pady=(0, 40))
        loan_treeview.bind("<ButtonRelease-1>", lambda event: select_loan(event, *entries, loan_id_entry=None, treeview=loan_treeview))

        treeviews.append(loan_treeview)
    
    return right_frame, treeviews