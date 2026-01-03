from database import connect_database
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from tkinter import * 
from books import search_book, decrease_book_quantity, increase_book_quantity, create_book_treeview, make_optional, search_book_title_author, make_optional
from books import select_data as select_book_data
from books import treeview_data as book_treeview_data
from students import search_student, create_student_treeview, search_bar
from students import select_student as select_student_data
from students import treeview_data as student_treeview_data
import sqlite3, datetime

flag = False # For clearing fields

def treeview_data():
    global loan_treeview
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

        loan_treeview.delete(*loan_treeview.get_children())
        for row in results:
            loan_treeview.insert("", END, iid=row["loan_id"], values=(
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

def create_loan_treeview(parent_frame):
    global loan_treeview
    
    vertical_scrollbar = Scrollbar(parent_frame, orient=VERTICAL)
    loan_treeview = ttk.Treeview(parent_frame, columns=("student_id", "student_name", "book_name", "loan_date", "return_date", "status"), show="headings", yscrollcommand=vertical_scrollbar)
    vertical_scrollbar.pack(side=RIGHT, fill=Y, pady=(10,0))
    vertical_scrollbar.config(command=loan_treeview.yview)
    loan_treeview.heading("student_id", text="Student ID", anchor="w")
    loan_treeview.heading("student_name", text="Student Name", anchor="w")
    loan_treeview.heading("book_name", text="Book Name", anchor="w")
    loan_treeview.heading("loan_date", text="Loan Date", anchor="w")
    loan_treeview.heading("return_date", text="Return Date", anchor="w")
    loan_treeview.heading("status", text="Status", anchor="w")

    loan_treeview.column("student_id", width=100, anchor="w")
    loan_treeview.column("student_name", width=150, anchor="w")
    loan_treeview.column("book_name", width=200, anchor="w")
    loan_treeview.column("loan_date", width=120, anchor="w")
    loan_treeview.column("return_date", width=120, anchor="w")
    loan_treeview.column("status", width=100, anchor="w")

    treeview_data()
    return loan_treeview

def loans_form(root):
    global student_treeview, book_treeview, right_frame, backbutton_image, add_button, delete_button, update_button
    global student_id_entry, book_name_entry, loan_date_entry, return_date_entry, status_combobox

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

    # Start of left frame
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
                        width=12, command=lambda: add_loan(student_id_entry, book_name_entry, loan_date_entry, return_date_entry))
    add_button.grid(row=5, column=0, columnspan=1, padx=(5,0), pady=20)

    update_button = Button(left_frame, text="Update", font=("times new roman", 12, "bold"), bg="#0B5345", fg="white", cursor="hand2",
                        width=12, command=lambda: update_loan(student_id_entry.get(), book_name_entry.get(), loan_date_entry.get_date().strftime("%y-%m-%d"), return_date_entry.get_date().strftime("%y-%m-%d"), status_combobox.get()))
    update_button.grid(row=5, column=1, columnspan=1, padx=(5,0),pady=10)
    update_button.config(state=DISABLED)

    delete_button = Button(left_frame, text="Delete", font=("times new roman", 12, "bold"), bg="#0B5345", fg="white", cursor="hand2",
                        width=12, command=lambda: delete_loan(student_id_entry.get(), book_name_entry.get()))   
    delete_button.grid(row=6, column=0, columnspan=1, padx=(5,0),pady=10)
    delete_button.config(state=DISABLED)

    clear_button = Button(left_frame, text="Clear", font=("times new roman", 12, "bold"), bg="#0B5345", fg="white", cursor="hand2",
                        width=12, command=lambda: clear_fields(student_id_entry, book_name_entry, loan_date_entry, return_date_entry, flag))
    clear_button.grid(row=6, column=1, columnspan=1, padx=(5,0), pady=10)

    view_loans_button = Button(left_frame, text="View Loans", font=("times new roman", 12, "bold"), bg="#0B5345", fg="white", cursor="hand2",
                        width=15, command=lambda: show_loans())
    view_loans_button.grid(row=7, column=0, columnspan=2, pady=10)
    # End of left frame

    # Start of right frame
    right_frame = build_right_frame(loans_frame)
    # End of right frame

def add_loan(student_id_entry, book_name_entry, loan_date_entry, return_date_entry):
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

        cursor.execute(
            "INSERT INTO LOANS (student_id, book_id, loan_date, return_date, status) VALUES (%s, %s, %s, %s, %s)",
            (student_id, book_id, loan_date, return_date, "active")
        )
        conn.commit()
        decrease_book_quantity(book_name)
        student_treeview_data()
        book_treeview_data()
        clear_fields(student_id_entry, book_name_entry, loan_date_entry, return_date_entry, False)
        messagebox.showinfo("Success", "Loan recorded successfully.")
    except Exception as e:
        print(e)
        messagebox.showerror("Error", f"error: {str(e)}")
    finally:
        conn.close()

def update_loan(student_id, book_name, loan_date, return_date, status):
    if not student_id or not book_name:
        messagebox.showwarning("Warning", "Please select a loan from the record.")
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
        if status == "returned":
            increase_book_quantity(book_name, "")
        clear_fields(student_id_entry, book_name_entry, loan_date_entry, return_date_entry, True)
        treeview_data()

    except Exception as e:
        messagebox.showerror("Error", f"error: {str(e)}")
    finally:
        conn.close()

def delete_loan(student_id, book_name):
    if not student_id or not book_name:
        messagebox.showwarning("Warning", "Please select a loan from the record.")
        return
    
    try:
        conn, cursor = connect_database()

        cursor.execute("""
            DELETE FROM LOANS
            WHERE student_id = %s
              AND book_id = (
                  SELECT b.id
                  FROM BOOKS b
                  WHERE b.title = %s
              )
        """, (student_id, book_name))

        conn.commit()
        messagebox.showinfo("Success", "Loan deleted successfully.")
        clear_fields(student_id_entry, book_name_entry, loan_date_entry, return_date_entry, True)
        treeview_data()
        increase_book_quantity(book_name, "")
    except Exception as e:
        messagebox.showerror("Error", f"error: {str(e)}")
    finally:
        conn.close()

def search_loan(search_combobox, search_entry):
    global loan_treeview
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

        loan_treeview.delete(*loan_treeview.get_children())
        for row in results:
            loan_treeview.insert("", END, values=(
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
    finally:
        if conn:
            conn.close()
  
def show_loans():
    global right_frame, loan_treeview, back_button_image, flag

    for widget in right_frame.winfo_children():
        widget.destroy()

    search_frame = Frame(right_frame, bg="white")
    search_frame.pack(fill=X, anchor="n", pady=10)

    back_button_image = PhotoImage(file="images\\go-back.png")
    back_button = Button(search_frame, image=back_button_image, cursor="hand2",
                            command=lambda: build_right_frame(right_frame, True),
                            bg="white", bd=0)
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
    search_entry_frame.grid_propagate(False)  # prevent resizing

    # Default widget inside the frame
    search_entry = Entry(search_entry_frame, font=("times new roman", 12), bd=2, bg="light gray")
    search_entry.pack(fill="both", expand=True)
    make_optional(search_entry)

    def update_search_entry(event):
        global new_entry
        # Clear the frame
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

    search_button = Button(search_frame, text="Search", font=("times new roman", 12),
                              bg="#0B5345", fg="white", cursor="hand2", width=10, command=lambda: search_loan(search_combobox.get(), new_entry.get()))
    search_button.grid(row=0, column=3, padx=20, pady=5)

    showall_button = Button(search_frame, text="Show All", font=("times new roman", 12),
                               bg="#0B5345", fg="white", cursor="hand2", width=10,
                               command=lambda: treeview_data())
    showall_button.grid(row=0, column=4, pady=5)

    delete_button.config(state=ACTIVE)
    update_button.config(state=ACTIVE)
    add_button.config(state=DISABLED)

    flag = True # For clearing fields

    loan_treeview = create_loan_treeview(right_frame)
    loan_treeview.pack(fill=BOTH, expand=1, anchor="n", pady=(0, 40))
    loan_treeview.bind("<ButtonRelease-1>", lambda event: select_loan(event, student_id_entry, book_name_entry, loan_date_entry, return_date_entry, status_combobox))

def select_loan(event, student_id_entry, book_name_entry, loan_date_entry, return_date_entry, status_combobox, loan_id_entry=None):
    global loan_treeview
    selected_item = loan_treeview.focus()
    if not selected_item:
        return
    
    # Capture the loan_id from iid
    loan_id = selected_item  

    if loan_id_entry:
        values = loan_treeview.item(selected_item, 'values')

        student_id_entry.insert(0, values[0])
        student_id_entry.config(state='disabled')

        book_name_entry.insert(0, values[2])
        book_name_entry.config(state='disabled')

        loan_id_entry.insert(0, loan_id)
        return
    
    clear_fields(student_id_entry, book_name_entry, loan_date_entry, return_date_entry, True)
    values = loan_treeview.item(selected_item, 'values')

    student_id_entry.insert(0, values[0])
    student_id_entry.config(state='disabled')

    book_name_entry.insert(0, values[2])
    book_name_entry.config(state='disabled')

    loan_date_entry.set_date(datetime.datetime.strptime(values[3], "%Y-%m-%d"))
    return_date_entry.set_date(datetime.datetime.strptime(values[4], "%Y-%m-%d"))

    status_combobox.set(values[5])
    
def build_right_frame(parent_frame, destroy=False):
    global right_frame, student_treeview, book_treeview, flag

    if destroy:
        for widget in right_frame.winfo_children():
            widget.destroy()

    right_frame = Frame(parent_frame, bg="white")
    right_frame.pack(side=RIGHT, fill=BOTH, expand=1)
    
    student_frame = Frame(right_frame, bg="white")
    student_frame.pack(fill=BOTH, expand=1)

    search_student_frame = Frame(student_frame, bg="white")
    search_student_frame.pack(fill=X, anchor="n")
    search_student_combo = ttk.Combobox(search_student_frame, values=["Id", "Name"], font=("times new roman", 12), state="readonly", justify=CENTER)
    search_student_combo.set("Search By")
    search_student_combo.grid(row=0, column=0, padx=10, pady=5)
    search_student_entry = Entry(search_student_frame, font=("times new roman", 12), bd=2, bg="light gray")
    search_student_entry.grid(row=0, column=1, pady=5)
    search_student_button = Button(search_student_frame, text="Search", font=("times new roman", 12), bg="#0B5345", fg="white", cursor="hand2"
                                , width=10, command=lambda: search_bar(search_student_combo.get(), search_student_entry.get()))
    search_student_button.grid(row=0, column=2, padx=20, pady=5)
    showall_student_button = Button(search_student_frame, text="Show All", font=("times new roman", 12), bg="#0B5345", fg="white", cursor="hand2"
                                , width=10, command=lambda: student_treeview_data())
    showall_student_button.grid(row=0, column=3, pady=5)

    student_treeview = create_student_treeview(student_frame)
    student_treeview.pack(fill=BOTH, expand=1, anchor="s")
    student_treeview.bind("<ButtonRelease-1>", lambda event: select_student_data(event, student_id_entry, None, None, None, None, None))

    book_frame = Frame(right_frame, bg="white")
    book_frame.pack(fill=BOTH, expand=1, pady=10)

    search_book_frame = Frame(book_frame, bg="white")
    search_book_frame.pack(fill=X, anchor="n")
    search_book_combo = ttk.Combobox(search_book_frame, values=["Title", "Author"], font=("times new roman", 12), state="readonly", justify=CENTER)
    search_book_combo.set("Search By")
    search_book_combo.grid(row=0, column=0, padx=10, pady=5)
    search_book_entry = Entry(search_book_frame, font=("times new roman", 12), bd=2, bg="light gray")
    search_book_entry.grid(row=0, column=1, pady=5)
    search_book_button = Button(search_book_frame, text="Search", font=("times new roman", 12), bg="#0B5345", fg="white", cursor="hand2",
                                width=10, command=lambda: search_book_title_author(search_book_combo.get(), search_book_entry.get()))
    search_book_button.grid(row=0, column=2, padx=20, pady=5)
    showall_book_button = Button(search_book_frame, text="Show All", font=("times new roman", 12), bg="#0B5345", fg="white", cursor="hand2",
                                width=10, command=lambda: book_treeview_data())
    showall_book_button.grid(row=0, column=3, pady=5)
    
    delete_button.config(state=DISABLED)
    update_button.config(state=DISABLED)
    add_button.config(state=ACTIVE)

    book_treeview = create_book_treeview(book_frame)
    book_treeview.pack(fill=X, expand=1, anchor="s")
    book_treeview.bind("<ButtonRelease-1>", lambda event: select_book_data(event, book_name_entry, None, None, None, None))
   
    make_optional(search_student_entry)
    make_optional(search_book_entry)

    flag = False # For clearing fields
    return right_frame
    
def clear_fields(student_id_entry, book_name_entry, loan_date_entry, return_date_entry, check):
    student_id_entry.config(state='normal')
    student_id_entry.delete(0, END)
    book_name_entry.config(state='normal')
    book_name_entry.delete(0, END)
    loan_date_entry.set_date(datetime.datetime.now())
    return_date_entry.set_date(datetime.datetime.now())
    if not check:
        book_treeview.selection_remove(book_treeview.selection())
        student_treeview.selection_remove(student_treeview.selection())
    else:
        loan_treeview.selection_remove(loan_treeview.selection())
