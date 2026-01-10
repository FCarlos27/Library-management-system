from database import connect_database
from tkinter import *
from tkinter import messagebox, ttk
from books import make_optional
from students import search_student
from loans import create_loan_treeview, select_loan, treeview_data as loan_treeview_data

def treeview_data():
    global penalty_treeview
    try:
        conn, cursor = connect_database()
        cursor.execute("""
        SELECT 
            P.id AS penalty_id,
            S.id AS student_id,
            S.name AS student_name,
            B.title AS book_title,
            P.reason AS reason,
            P.penalty_date AS date_issued,
            P.amount AS amount
        FROM PENALTIES P
        JOIN LOANS L ON P.loan_id = L.id
        JOIN STUDENTS S ON L.student_id = S.id
        JOIN BOOKS B ON L.book_id = B.id
    """)
        results = cursor.fetchall()
        penalty_treeview.delete(*penalty_treeview.get_children())
        for row in results:
            penalty_treeview.insert("", END, values=(
                row["penalty_id"],
                row["student_id"],
                row["student_name"],
                row["book_title"],
                row["reason"],
                row["date_issued"],
                row["amount"]
            ))
    except Exception as e:
        return e 
    finally:
        if conn: 
            conn.close()

def create_penalty_treeview(parent_frame: Frame) -> ttk.Treeview:
    global penalty_treeview

    vertical_scrollbar = Scrollbar(parent_frame, orient=VERTICAL)
    penalty_treeview = ttk.Treeview(parent_frame, columns=("Penalty ID", "Student ID", "Student Name", "Book Title", "Reason", "Date Issued", "Amount"), show="headings", yscrollcommand=vertical_scrollbar.set)
    vertical_scrollbar.config(command=penalty_treeview.yview)
    vertical_scrollbar.pack(pady=(10,0), side=RIGHT, fill=Y)
    penalty_treeview.heading("Penalty ID", text="Penalty ID", anchor="w")
    penalty_treeview.heading("Student ID", text="Student ID", anchor="w")
    penalty_treeview.heading("Student Name", text="Student Name", anchor="w")
    penalty_treeview.heading("Book Title", text="Book Title", anchor="w")
    penalty_treeview.heading("Reason", text="Reason", anchor="w")
    penalty_treeview.heading("Date Issued", text="Date Issued", anchor="w")
    penalty_treeview.heading("Amount", text="Amount", anchor="w")

    penalty_treeview.column("Penalty ID", width=80, anchor="w")
    penalty_treeview.column("Student ID", width=80, anchor="w")
    penalty_treeview.column("Student Name", width=150, anchor="w")
    penalty_treeview.column("Book Title", width=150, anchor="w")
    penalty_treeview.column("Reason", width=200, anchor="w")
    penalty_treeview.column("Date Issued", width=100, anchor="w")
    penalty_treeview.column("Amount", width=80, anchor="w")

    treeview_data()
    return penalty_treeview

def penalties_form(root):
    global backbutton_image, created, top_frame, active_tree, buttons, treeview, bot_frame, fields, bot_frame
    
    fields = [
    {"name": "student_id_entry", "text": "Student ID", "widget_type": "entry", "row": 0, "col": 0},
    {"name": "book_title_entry", "text": "Book Title", "widget_type": "entry", "row": 0, "col": 2},
    {"name": "loan_id_entry", "text": "Loan ID", "widget_type": "entry", "row": 1, "col": 0},
    {"name": "amount_entry", "text": "Amount", "widget_type": "entry", "row": 1, "col": 2},
    {"name": "reason_entry", "text": "Reason", "widget_type": "text", "row": 2, "col": 0},]
    
    fields2 = [
        {"name": "student_id_entry", "text": "Student ID", "widget_type": "entry", "row": 0, "col": 0},
        {"name": "book_title_entry", "text": "Book Title", "widget_type": "entry", "row": 0, "col": 2},
        {"name": "penalty_id_entry", "text": "Penalty ID", "widget_type": "entry", "row": 1, "col": 0},
        {"name": "amount_entry", "text": "Amount", "widget_type": "entry", "row": 1, "col": 2},
        {"name": "reason_entry", "text": "Reason", "widget_type": "text", "row": 2, "col": 0},
        {"name": "date_issued_entry", "text": "Date Issued", "widget_type": "entry", "row": 2, "col": 2},
    ]

    buttons = [
        {"name": "add_bttn", "text": "Add", "row": 3, "col": 0,
        "command": lambda: add_penalty(
            created["student_id_entry"], created["book_title_entry"],
            created["loan_id_entry"], created["reason_entry"], created["amount_entry"], treeview)},
        {"name": "update_bttn", "text": "Update", "row": 3, "col": 1,
        "command": lambda: update_penalty(
            created["penalty_id_entry"], created["student_id_entry"], created["book_title_entry"],
            created["reason_entry"], created["date_issued_entry"], treeview, created["amount_entry"])},
        {"name": "delete_bttn", "text": "Delete", "row": 3, "col": 2,
        "command": lambda: delete_penalty(
            created["penalty_id_entry"], created["student_id_entry"], created["book_title_entry"],
            created["reason_entry"], created["date_issued_entry"], treeview, created["amount_entry"])},
        {"name": "clear_bttn", "text": "Clear", "row": 3, "col": 3,
       "command": lambda: clear_fields(created.get("student_id_entry"), created.get("book_title_entry"), created.get("loan_id_entry"),
            created.get("amount_entry"), created.get("reason_entry"), created.get("date_issued_entry"), created.get("penalty_id_entry"), treeview=treeview, check=True)},
        {"name": "show_penalties_bttn", "text": "View Penalties", "row": 4, "col": 1,
            "columnspan": 2, "command": lambda: show_penalties(top_frame, bot_frame, fields2, buttons)}]

    penalties_frame = Frame(root, bg="white", bd=2, relief=RIDGE)
    penalties_frame.place(x=205, y=98, relheight=1, width=1065)
    header_frame = Frame(penalties_frame, bg="#0B5345", height=40)
    header_frame.pack(fill=X)

    header = Label(header_frame, text="Penalties Management", font=("times new roman", 15, 'bold'), bg="#0B5345", fg="white", anchor=CENTER)
    header.grid(row=0, column=1, sticky="W", padx=350)

    backbutton_image = PhotoImage(file="images\\return.png")
    back_button = Button(header_frame, image=backbutton_image, cursor="hand2", bg="#0B5345",bd=0, command=lambda: penalties_frame.destroy())
    back_button.grid(row=0, column=0, padx=5)
    
    bot_frame, created = build_bot_frame(penalties_frame, fields, buttons, pack=False)
    top_frame, treeview = build_top_frame(penalties_frame, created, create_loan_treeview, pack=True)

    bot_frame.pack()
    

def build_top_frame(parent_frame: Frame, created: dict, treeview_factory: callable, pack: bool, destroy: bool = False) -> Frame:
    global  active_tree, back_button_image

    if destroy:
        for widget in parent_frame.winfo_children():
            widget.destroy()

    # Decide active tree based on factory name
    active_tree = "loan" if treeview_factory.__name__ == "create_loan_treeview" else "penalty"

    top_frame = Frame(parent_frame, bg="white")
    top_frame.pack(fill=X)

    search_frame = Frame(top_frame, bg="white")
    search_frame.pack()

    search_combobox = ttk.Combobox(
        search_frame,
        values=("Student Id", "Student Name", "Book Title"),
        font=("times new roman", 12),
        state="readonly",
        justify=CENTER
    )
    search_combobox.set("Search By")
    search_combobox.grid(row=0, column=1, padx=20)

    search_entry = Entry(search_frame, font=("times new roman", 12), bg="light gray")
    search_entry.grid(row=0, column=2)
    make_optional(search_entry)

    search_bttn = Button(search_frame, text="SEARCH", font=("times new roman", 12),
           bg="#0B5345", fg="white", width=10, cursor="hand2", 
           command=lambda: search_bar(search_combobox.get(), search_entry, treeview))
    search_bttn.grid(row=0, column=3, padx=20)

    show_all_bttn = Button(search_frame, text="Show All", font=("times new roman", 12),
           bg="#0B5345", fg="white", width=10, cursor="hand2", command=lambda: treeview_data() if active_tree == "penalty" else loan_treeview_data())
    show_all_bttn.grid(row=0, column=4)

    # Treeview is created by the factory function you pass in
    treeview = treeview_factory(top_frame)
    treeview.pack(pady=(10,0), fill=BOTH, expand=True)

    # Bind and active buttons depending on active tree
    if active_tree == "loan":
        student_id_entry = created.get("student_id_entry")
        book_title_entry = created.get("book_title_entry")
        loan_id_entry = created.get("loan_id_entry")
        reason_entry = created.get("reason_entry")
        amount_entry = created.get("amount_entry")
        treeview.bind("<ButtonRelease-1>", lambda event: [clear_fields(student_id_entry, book_title_entry, loan_id_entry, reason_entry, amount_entry, treeview=treeview, check=False),
            select_loan(event, student_id_entry, book_title_entry, None, None, None, loan_id_entry=loan_id_entry)])
        
        created["update_bttn"].config(state="disabled")
        created["delete_bttn"].config(state="disabled")

    else:
        treeview.bind("<ButtonRelease-1>", lambda event: select_penalty(
            event,
            created["penalty_id_entry"],
            created["student_id_entry"],
            created["book_title_entry"],
            created["reason_entry"],
            created["date_issued_entry"],
            created["amount_entry"],
            treeview=treeview))

        back_button_image = PhotoImage(file="images\\go-back.png")
        back_button = Button(search_frame, image=back_button_image, cursor="hand2",
                command=lambda: back_to_loans(top_frame, bot_frame, fields, buttons), 
                bg="white", bd=0
            )
        back_button.grid(row=0, column=0, padx=10, pady=5)
    
        created["add_bttn"].config(state="disabled")
        created["show_penalties_bttn"].config(state="disabled")

    if pack:
        top_frame.pack(fill=X)

    return top_frame, treeview


def build_bot_frame(parent: Frame, fields: list, buttons: list, pack: bool, destroy: bool = False) -> tuple[Frame, dict]:
    """
    Create a form inside a frame with given fields and buttons.
    
    fields: list of dicts with keys: text, widget_type, row, col
    buttons: list of dicts with keys: text, command, row, col
    """

    if destroy:
        for widget in parent.winfo_children():
            widget.destroy()

    bot_frame = Frame(parent, bg="white")
    inner_frame = Frame(bot_frame, bg="white")
    inner_frame.pack()

    created_widgets = {}

    # Create labels + entries/texts
    for field in fields:
        Label(inner_frame, text=field["text"], font=("times new roman", 12), bg="white").grid(row=field["row"], column=field["col"])
        
        if field["widget_type"] == "entry":
            widget = Entry(inner_frame, font=("times new roman", 12), bg="white")
        elif field["widget_type"] == "text":
            widget = Text(inner_frame, font=("times new roman", 12), bg="white", height=3, width=20)
        else:
            raise ValueError("Unsupported widget type")
        
        widget.grid(row=field["row"], column=field["col"]+1, padx=20, pady=10)
        created_widgets[field["name"]] = widget

    # Create buttons
    for btn in buttons:
        b = Button(inner_frame, text=btn["text"], font=("times new roman", 12, "bold"),
                   width=15, fg="white", bg="#0B5345", cursor="hand2", command=btn.get("command"))
        b.grid(row=btn["row"], column=btn["col"], columnspan=btn["columnspan"] if btn.get("columnspan") else 1, 
               padx=btn.get("padx", (20, 0)) if btn["name"] not in ("add_bttn", "show_penalties_bttn") else 0, 
               pady=btn.get("pady", 15) if btn["name"] != "show_penalties_bttn" else 0)
        created_widgets[btn["name"]] = b

    if pack:
        bot_frame.pack()

    return bot_frame, created_widgets

def add_penalty(student_id_entry, book_title_entry, loan_id_entry, reason_entry, amount_entry=0.0, tree=None):
    student_id = student_id_entry.get()
    loan_id = loan_id_entry.get()
    reason = reason_entry.get("1.0", END).strip()
    amount = amount_entry.get()

    if not (student_id and loan_id and reason):
        messagebox.showwarning("Incomplete Info", "All fields are required")
        return
    
    if search_student(student_id) is None:
        messagebox.showerror("Error", "Student ID does not exist")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number")
        return

    if loan_id is None:
        messagebox.showerror("Error", "Select a valid Loan ID from the Loans section")
        return
    else:
            conn, cursor = connect_database()
            cursor.execute("SELECT * FROM LOANS WHERE id = %s AND student_id = %s", (loan_id, student_id))
            result = cursor.fetchone()
            if result is None:
                messagebox.showerror("Error", "The selected Loan ID does not belong to the specified Student ID")
                conn.close()
                return
            
    try:
        conn, cursor = connect_database()
        cursor.execute("""
            INSERT INTO PENALTIES (student_id, loan_id, reason, amount)
            VALUES (%s, %s, %s, %s)
        """, (student_id, loan_id, reason, amount))
        cursor.execute("""
            UPDATE STUDENTS
            SET total_penalty = total_penalty + 1
            WHERE id = %s
        """, (student_id,))
        conn.commit()
        clear_fields(student_id_entry, book_title_entry, loan_id_entry, 
                     amount_entry, reason_entry, treeview=tree, check=True)
        messagebox.showinfo("Success", "Penalty added successfully")
        return None
    except Exception as e:
        conn.rollback()
        return e
    finally:
        if conn:
            conn.close()

def update_penalty(penalty_id_entry, student_id_entry, book_title_entry,reason_entry, date_issued_entry, tree, amount_entry=None):
    penalty_id = penalty_id_entry.get()
    reason = reason_entry.get("1.0", END).strip()
    date_issued = date_issued_entry.get()
    amount = amount_entry.get() if amount_entry else None

    if not [penalty_id, reason, date_issued]:
        messagebox.showwarning("Incomplete Info", "All fields are required")
        return

    try:
        conn, cursor = connect_database()
        if amount is not None:
            cursor.execute("""
                UPDATE PENALTIES
                SET reason = %s, penalty_date = %s, amount = %s
                WHERE id = %s
                """, (reason, date_issued, amount, penalty_id))
        else:
            cursor.execute("""
                UPDATE PENALTIES
                SET reason = %s, date_issued = %s
                WHERE id = %s
                """, (reason, date_issued, penalty_id))
        conn.commit()
        messagebox.showinfo("Success", "Penalty updated successfully")
        clear_fields(penalty_id_entry, student_id_entry, book_title_entry, reason_entry, date_issued_entry, amount_entry, treeview=tree, check=True)
        treeview_data()
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Error", f"Failed to update penalty: {e}")
    finally:
        if conn:
            conn.close()

def delete_penalty(penalty_id_entry, student_id_entry, book_title_entry,reason_entry, date_issued_entry, tree, amount_entry=None):
    index = tree.selection()
    content = tree.item(index)
    row = content['values']
    id_penalty = row[0]
    result = messagebox.askquestion("Delete Confirmation", "Are you sure you want to delete this penalty?")

    if not id_penalty:
        messagebox.showwarning("Incomplete Info", "Penalty ID is required")
        return
    
    if result:
        try:
            conn, cursor = connect_database()
            cursor.execute("DELETE FROM PENALTIES WHERE id = %s", (id_penalty,))
            cursor.execute("UPDATE STUDENTS SET total_penalty = total_penalty - 1 WHERE id = %s", (student_id_entry.get(),))
            conn.commit()
            messagebox.showinfo("Success", "Penalty deleted successfully")
            clear_fields(penalty_id_entry, student_id_entry, book_title_entry, reason_entry, date_issued_entry, amount_entry, treeview=tree, check=True)
            treeview_data()
            return
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"Failed to delete penalty: {e}")
        finally:
            if conn:
                conn.close()

def show_penalties(top_frame: Frame, bottom_frame: Frame, fields: list, buttons: list):
    global treeview, created

    bot_frame, new_created = build_bot_frame(bottom_frame, fields, buttons, pack=False, destroy=True)
    top_frame, new_treeview = build_top_frame(top_frame, new_created, create_penalty_treeview, pack=True, destroy=True)
    
    bot_frame.pack()
    treeview_data()

    treeview = new_treeview
    created.update(new_created)

def back_to_loans(top_frame: Frame, bottom_frame: Frame, fields: list, buttons: list):
    global treeview, created

    bot_frame, new_created = build_bot_frame(bottom_frame, fields, buttons, pack=False, destroy=True)
    top_frame, new_treeview = build_top_frame(top_frame, new_created, create_loan_treeview, pack=True, destroy=True)
    
    bot_frame.pack()
    loan_treeview_data()

    treeview = new_treeview
    created.update(new_created)

def select_penalty(event, *entries, treeview=None):
    index = treeview.selection()
    if not index: 
        return
    content = treeview.item(index)
    row = content['values']
    # remove column 2 (Student Name)
    row_filtered = [val for i, val in enumerate(row) if i != 2]

    clear_fields(*entries, treeview=treeview, check=False)

    # Fill entries with filtered row values
    for i, (entry, value) in enumerate(zip(entries, row_filtered)):
        if isinstance(entry, Text):
            entry.config(state='normal')
            entry.insert("1.0", value)
        else:
            entry.config(state='normal')
            entry.insert(0, value)

        # Disable the first 3 entries after filling
        if i < 3:
            entry.config(state='disabled')

def search_bar(search_by: str, search_entry: Entry, treeview: ttk.Treeview):
    if search_by == "Search By" or not search_entry.get().strip():
        messagebox.showwarning("Error", "Please select a search term.")
        return
    
    if not search_entry.get().strip():
        messagebox.showwarning("Invalid Selection", "Please select an option.")
        return
    
    try:
        conn, cursor = connect_database()
        if active_tree == "loan":
            if search_by == "Student Id":
                cursor.execute("""SELECT L.student_id, S.name AS student_name, B.title AS book_name, L.loan_date, L.return_date, L.status
                                FROM LOANS L JOIN STUDENTS S ON L.student_id = S.id JOIN BOOKS B ON L.book_id = B.id
                                WHERE L.student_id = %s""", 
                                (search_entry.get().strip(),))
            
            elif search_by == "Student Name":
                cursor.execute("""
                    SELECT L.student_id, S.name AS student_name, B.title AS book_name, L.loan_date, L.return_date, L.status
                    FROM LOANS L
                    JOIN STUDENTS S ON L.student_id = S.id
                    JOIN BOOKS B ON L.book_id = B.id
                    WHERE S.name LIKE %s
                """, ('%' + search_entry.get().strip() + '%',))
            
            elif search_by == "Book Title":
                cursor.execute("""
                    SELECT L.student_id, S.name AS student_name, B.title AS book_name, L.loan_date, L.return_date, L.status
                    FROM LOANS L
                    JOIN BOOKS B ON L.book_id = B.id
                    JOIN STUDENTS S ON L.student_id = S.id
                    WHERE B.title LIKE %s
                """, ('%' + search_entry.get().strip() + '%',))

            results = cursor.fetchall()
            treeview.delete(*treeview.get_children())
            for row in results:
                treeview.insert("", END, values=(
                    row["student_id"],
                    row["student_name"],
                    row["book_name"],
                    row["loan_date"],
                    row["return_date"],
                    row["status"]
                ))
        else:
            if search_by == "Student Id":
                cursor.execute("""
                    SELECT 
                        P.id AS penalty_id,
                        S.id AS student_id,
                        S.name AS student_name,
                        B.title AS book_title,
                        P.reason AS reason,
                        P.penalty_date AS date_issued,
                        P.amount AS amount
                    FROM PENALTIES P
                    JOIN LOANS L ON P.loan_id = L.id
                    JOIN STUDENTS S ON L.student_id = S.id
                    JOIN BOOKS B ON L.book_id = B.id
                    WHERE S.id = %s
                    """, (search_entry.get().strip(),))
                
            elif search_by == "Student Name":
                cursor.execute("""
                    SELECT 
                        P.id AS penalty_id,
                        S.id AS student_id,
                        S.name AS student_name,
                        B.title AS book_title,
                        P.reason AS reason,
                        P.penalty_date AS date_issued,
                        P.amount AS amount
                    FROM PENALTIES P
                    JOIN LOANS L ON P.loan_id = L.id
                    JOIN STUDENTS S ON L.student_id = S.id
                    JOIN BOOKS B ON L.book_id = B.id
                    WHERE S.name LIKE %s
                    """, ('%' + search_entry.get().strip() + '%',))
                
            elif search_by == "Book Title":
                cursor.execute("""
                    SELECT 
                        P.id AS penalty_id,
                        S.id AS student_id,
                        S.name AS student_name,
                        B.title AS book_title,
                        P.reason AS reason,
                        P.penalty_date AS date_issued,
                        P.amount AS amount
                    FROM PENALTIES P
                    JOIN LOANS L ON P.loan_id = L.id
                    JOIN STUDENTS S ON L.student_id = S.id
                    JOIN BOOKS B ON L.book_id = B.id
                    WHERE B.title LIKE %s
                    """, ('%' + search_entry.get().strip() + '%',))
            
            results = cursor.fetchall()
            treeview.delete(*treeview.get_children())
            for row in results:
                treeview.insert("", END, values=(
                    row["penalty_id"],
                    row["student_id"],
                    row["student_name"],
                    row["book_title"],
                    row["reason"],
                    row["date_issued"],
                    row["amount"]
                ))

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

def clear_fields(*entries, treeview: ttk.Treeview = None, check: bool):
    for entry in entries:
        if entry is None:
            continue
        try:
            entry.config(state="normal")
            if isinstance(entry, Text):
                entry.delete("1.0", "end")
            else:
                entry.delete(0, "end")
        except TclError:
            continue

    if check and treeview:
        treeview.selection_remove(treeview.selection())
