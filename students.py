from database import connect_database
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from tkinter import *
from books import make_optional
from datetime import datetime 
import re

def treeview_data(treeview: ttk.Treeview) -> None:
    """
    Populate the given Treeview widget with student records from the database.
    
    Parameters
    ----------
    treeview : Treeview widget to populate with student data.
    """
    try:
        conn, cursor = connect_database()
        cursor.execute("SELECT * FROM STUDENTS")
        results = cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for row in results:
            treeview.insert("", END, values=(
                row["id"],
                row["name"],
                row["birthdate"],
                row["phone"],
                row["email"],
                row["address"],
                row["total_penalty"]
            ))
    except Exception as e:
        return e
    finally:
        conn.close()

def create_student_treeview(parent_frame: Frame) -> ttk.Treeview:
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
    # Configure headings and column widths for readability.

    vertical_scrollbar = Scrollbar(parent_frame, orient=VERTICAL)
    student_treeview = ttk.Treeview(parent_frame, columns=("id", "name", "birthdate", "phone", "email", "address", "total_penalty"), show="headings")
    
    vertical_scrollbar.pack(side=RIGHT, fill=Y, pady=(10,0))
    vertical_scrollbar.config(command=student_treeview.yview)

    # Define column headers

    student_treeview.heading("id", text="Id", anchor="w")
    student_treeview.heading("name", text="Name", anchor="w")
    student_treeview.heading("birthdate", text="Birthdate", anchor="w")
    student_treeview.heading("phone", text="Phone", anchor="w")
    student_treeview.heading("email", text="Email", anchor="w")
    student_treeview.heading("address", text="Address", anchor="w")
    student_treeview.heading("total_penalty", text="Penalties", anchor="w")

    # Set column widths

    student_treeview.column("id", width=100, anchor="w")
    student_treeview.column("name", width=120, anchor="w")
    student_treeview.column("birthdate", width=60, anchor="w")
    student_treeview.column("phone", width=80, anchor="w")  
    student_treeview.column("email", width=200, anchor="w")
    student_treeview.column("address", width=120, anchor="w")
    student_treeview.column("total_penalty", width=60, anchor="w")
    
    treeview_data(student_treeview)
    return student_treeview

def student_form(root: Tk) -> None:
    """
    Build and display the Student Management interface inside the given root window.

    This function creates a dedicated frame for managing student records. It includes:
      - A header with a title and back button.
      - A top frame containing search controls (search by ID or Name, search entry, 
        search button, and show-all button).
      - A Treeview widget to display student data.
      - A bottom frame with entry fields for student details (ID, Name, Birthdate, 
        Phone, Email, Address).
      - Action buttons to add, update, delete, and clear student records.

    Parameters
    ----------
    root : Tk
        The main application window where the student management frame will be placed.

    Notes
    -----
    - The function uses global `backbutton_image` for the back button icon.
    - The Treeview is bound to `select_student` for row selection.
    - Buttons trigger helper functions (`add_student`, `update_student`, 
      `delete_student`, `clear_fields`) to manage student data.
    - The function does not return a value; it directly modifies the GUI.
    """
    global backbutton_image

    students_frame = Frame(root,bg="white", bd=2, relief=RIDGE)
    students_frame.place(x=205, y= 98, relheight=1, width=1065)
    header_frame = Frame(students_frame, bg="#2b7192", height=40)
    header_frame.pack(fill=X)

    header = Label(header_frame, text="Student Management", font=("times new roman", 15, 'bold'), bg="#2b7192", fg="white", anchor='center')
    header.grid(row=0, column=1, sticky="W", padx=350)

    backbutton_image = PhotoImage(file="images\\return.png")
    back_button = Button(header_frame, image=backbutton_image, cursor="hand2", bg="#2b7192",bd=0 , command=lambda: students_frame.destroy())
    back_button.grid(row=0, column=0, padx=5)
    
   # === Top Frame ===

    top_frame = Frame(students_frame, bg="#f0f9ff")
    top_frame.pack(fill=X)

    searchFrame = Frame(top_frame, bg="#f0f9ff")
    searchFrame.pack()
    search_combobox = ttk.Combobox(searchFrame, values=("Id","Name"), font=("times new roman", 12), state="readonly", justify="center")
    search_combobox.set("Search by")
    search_combobox.grid(row=0, column=0, padx= 20)
    search_entry = Entry(searchFrame,font=("times new roman", 12), bg="light gray")
    search_entry.grid(row=0, column=1)
    make_optional(search_entry)

    search_button = Button(searchFrame, text="SEARCH", font=('times new roman', 12), bg="#2b7192", fg="white", width=10,
                           cursor="hand2", command=lambda: search_bar(search_combobox.get(), search_entry.get(), student_treeview))
    search_button.grid(row=0, column=2, padx=20)

    showall_button = Button(searchFrame, text="Show All", font=('times new roman', 12), bg="#2b7192", fg="white", width=10, 
                            cursor="hand2", command=lambda: treeview_data(student_treeview))
    showall_button.grid(row=0, column=3)

    student_treeview = create_student_treeview(top_frame)
    student_treeview.pack(pady=(10, 0), fill=BOTH, expand=TRUE)

    student_treeview.bind("<ButtonRelease-1>", lambda event: select_student(event,  treeview=student_treeview, id_entry=s_id_entry, name_entry=s_name_entry, birthdate_entry=s_birthdate_entry,
                                                                        phone_entry=s_phone_entry, email_entry=s_email_entry, address_entry=s_address_entry))
    
    # === Bottom Frame ===

    bottom_frame = Frame(students_frame, bg="white")
    bottom_frame.pack()

    s_name = Label(bottom_frame, text="Name", font=("times new roman", 12), bg="white")
    s_name.grid(row=0, column=0)
    s_name_entry = Entry(bottom_frame, font=("times new roman", 12), bg="white")
    s_name_entry.grid(row=0, column=1, padx=20, pady=10)

    s_id = Label(bottom_frame, text="Id", font=("times new roman", 12), bg="white")
    s_id.grid(row=1, column=0)
    s_id_entry = Entry(bottom_frame, font=("times new roman", 12), bg="white")
    s_id_entry.grid(row=1, column=1, padx=20, pady=10)

    s_phone = Label(bottom_frame, text="Phone", font=("times new roman", 12), bg="white")
    s_phone.grid(row=2, column=0)
    s_phone_entry = Entry(bottom_frame, font=("times new roman", 12), bg="white")
    s_phone_entry.grid(row=2, column=1, padx=20, pady=10)

    s_birthdate = Label(bottom_frame, text="Birthdate", font=("times new roman", 12), bg="white")
    s_birthdate.grid(row=0, column=2)
    s_birthdate_entry = DateEntry(bottom_frame, width= 18, font=("times new roman",12), bg="white", date_pattern="YYYY-MM-DD")
    s_birthdate_entry.grid(row=0, column=3, padx=20, pady=10)
    
    s_email = Label(bottom_frame, text="Email", font=("times new roman", 12), bg="white")
    s_email.grid(row=1, column=2)
    s_email_entry = Entry(bottom_frame, font=("times new roman", 12), bg="white")
    s_email_entry.grid(row=1, column=3, padx=20, pady=10)

    s_address = Label(bottom_frame, text="Address", font=("times new roman", 12), bg="white")
    s_address.grid(row=2, column=2)
    s_address_entry = Entry(bottom_frame, font=("times new roman", 12), bg="white")
    s_address_entry.grid(row=2, column=3, padx=20, pady=10)

    add_btn = Button(bottom_frame, text="Add", font=("times new roman", 12, "bold"), width= 15, fg="white", 
        bg="#00566b", cursor="hand2", command=lambda: add_student(s_id_entry, s_name_entry, s_birthdate_entry,
                                                                   s_phone_entry, s_email_entry, s_address_entry, student_treeview))
    add_btn.grid(row=4, column=0, padx=0, pady=20)

    update_btn = Button(bottom_frame, text="Update", font=("times new roman", 12, "bold"), width= 15, fg="white",
        bg="#00566b",cursor="hand2", command=lambda: update_student(s_id_entry, s_name_entry, 
                                                                          s_birthdate_entry, s_phone_entry, s_email_entry, 
                                                                          s_address_entry, student_treeview))
    update_btn.grid(row=4, column=1, padx=(20,0), pady=20)

    delete_btn = Button(bottom_frame,text="Delete",font=("times new roman", 12, "bold"), width= 15, fg="white",
        bg="#00566b", cursor="hand2", command=lambda: delete_student(s_id_entry, s_name_entry, s_birthdate_entry,
                                                                     s_phone_entry, s_email_entry, s_address_entry, treeview=student_treeview))
    delete_btn.grid(row=4, column=2, padx=(20,0), pady=20)

    clear_btn = Button(bottom_frame, text="Clear", font=("times new roman", 12, "bold"), width= 15, fg="white",
        bg="#00566b", cursor="hand2", command=lambda: clear_fields(s_id_entry, s_name_entry, s_birthdate_entry,
                                                                   s_phone_entry, s_email_entry, s_address_entry, treeview=student_treeview, check=True))
    clear_btn.grid(row=4, column=3, padx=(20,0), pady=20)



def add_student(id_entry: Entry, name_entry: Entry, birthdate_entry: Entry, 
                phone_entry: Entry, email_entry: Entry, address_entry: Entry, treeview: ttk.Treeview) -> None:
    """
    Validate input fields and insert a new student record into the database.

    Parameters
    ----------
    id_entry : Entry widget containing the student ID.
    name_entry : Entry widget containing the student's name.
    birthdate_entry : Entry widget containing the student's birthdate in YYYY-MM-DD format.
    phone_entry : Entry widget containing the student's phone number.
    email_entry : Entry widget containing the student's email address.
    address_entry : Entry widget containing the student's address."""

    student_id = id_entry.get().strip()
    name = name_entry.get().strip()
    birthdate = birthdate_entry.get().strip()
    phone = phone_entry.get().strip()
    email = email_entry.get().strip()
    address = address_entry.get().strip()

    # Basic validation
    if not all([student_id, name, birthdate, phone, email, address]):
        messagebox.showerror("Incomplete Info", "Please complete all required fields.")
        return
    
    if not student_id.isdigit() or len(student_id) > 10:
        messagebox.showerror("Invalid ID", "Student ID should be a numeric value.")
        return
    
    if re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email) is None:
        messagebox.showerror("Invalid Email", "Please enter a valid email address.")
        return

    if search_student(student_id):
        messagebox.showerror("Duplicate ID", "A student with this ID already exists.")
        return

    try:
        birthdate = datetime.strptime(birthdate, "%Y-%m-%d").date()
        if birthdate > datetime.now().date():
            messagebox.showerror("Invalid Date", "Birthdate cannot be in the future.")
            return
        if (datetime.now().year - birthdate.year) < 10:
            messagebox.showerror("Invalid Date", "Student must be at least 10 years old.")
            return
    except ValueError:
        messagebox.showerror("Invalid Date", "Please enter birthdate in YYYY-MM-DD format.")
        return
    
    if not phone.isdigit() or len(phone) != 11:
        messagebox.showerror("Invalid Phone", "Phone number should contain only digits and be 11 digits long.")
        return

    try:
        conn, cursor = connect_database()
        cursor.execute(
            "INSERT INTO STUDENTS (id, name, birthdate, phone, email, address) VALUES (%s, %s, %s, %s, %s, %s)",
            (student_id, name, birthdate, phone, email, address)
        )
        conn.commit()
        treeview_data(treeview)
        clear_fields(id_entry, name_entry, birthdate_entry, phone_entry, email_entry, address_entry, treeview=treeview, check=True)
        messagebox.showinfo("Success", "Student added successfully.")
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

def update_student(id_entry: Entry, name_entry: Entry, birthdate_entry: Entry,
                    phone_entry: Entry, email_entry: Entry, address_entry: Entry, treeview: ttk.Treeview) -> None:
    """
    Update an existing student record in the database with new values from entry fields.

    This function retrieves the selected student ID from the Treeview, validates the
    updated input fields (email format, phone digits, birthdate validity, minimum age),
    and performs an SQL UPDATE operation. If successful, the student record is updated
    in the database and the Treeview is refreshed.

    Behavior
    --------
    - Shows error messages via `messagebox.showerror` if validation fails.
    - Ensures birthdate is not in the future and student is at least 10 years old.
    - Updates the STUDENTS table with new values for name, birthdate, phone, email, and address.
    - Displays a success message when the update completes.
    - Clears and resets entry fields using `clear_fields(...)`.
    - Refreshes the Treeview data via `treeview_data(...)`.
    """

    # Basic validation
    if not id_entry.get().strip():
        messagebox.showwarning("No Selection", "Please select a student to update.")
        return
    
    if re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email_entry.get()) is None:
        messagebox.showerror("Invalid Email", "Please enter a valid email address.")
        return
    
    if not phone_entry.get().isdigit():
        messagebox.showerror("Invalid Phone", "Phone number should contain only digits and be 10 digits long.")
        return

    try:
        birthdate = datetime.strptime(birthdate_entry.get(), "%Y-%m-%d").date()
        if birthdate > datetime.now().date():
            messagebox.showerror("Invalid Date", "Birthdate cannot be in the future.")
            return
        if (datetime.now().year - birthdate.year) < 10:
            messagebox.showerror("Invalid Date", "Student must be at least 10 years old.")
            return
    except ValueError:
        messagebox.showerror("Invalid Date", "Please enter birthdate in YYYY-MM-DD format.")
        return

    try: 
        conn, cursor = connect_database()
        cursor.execute("UPDATE STUDENTS SET name=%s, birthdate=%s, phone=%s, email=%s, address=%s WHERE id=%s", (
            name_entry.get(), birthdate_entry.get(), phone_entry.get(), email_entry.get(), address_entry.get(), id_entry.get()))
        conn.commit()
        messagebox.showinfo("Success", "Student updated successfully.")
        clear_fields(id_entry, name_entry, birthdate_entry, phone_entry, email_entry, address_entry, treeview=treeview, check=True)
        treeview_data(treeview)
        return
    except Exception as e:
        messagebox.showerror("Error", f"Invalid operation due to: {e}")
    finally:
        conn.close()

def delete_student(id_entry: Entry, name_entry: Entry, birthdate_entry: Entry,
                    phone_entry: Entry, email_entry: Entry, address_entry: Entry, treeview: ttk.Treeview) -> None:
    """
    Delete a student record from the database based on the selected ID.

    This function validates that a student is selected, checks if the student
    exists, and prompts the user for confirmation. If confirmed, the student
    record is removed from the STUDENTS table, the Treeview is refreshed, and
    the input fields are cleared.

    Behavior
    --------
    - Shows a warning if no student ID is selected.
    - Shows an error if the student ID does not exist in the database.
    - Prompts the user with a confirmation dialog before deletion.
    - Executes a SQL DELETE statement to remove the student record.
    - Displays a success message when deletion completes.
    - Clears entry fields and refreshes the Treeview data.
    """
    # Basic validation
    if not id_entry.get().strip():
        messagebox.showwarning("No Selection", "Please select a student to delete.")
        return
    
    if search_student(id_entry.get().strip()) is None:
        messagebox.showerror("Not Found", "Student with this ID does not exist.")
        return
    
    result = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this student?")
    if result:
        try: 
            conn, cursor = connect_database()
            cursor.execute("DELETE FROM STUDENTS WHERE id=%s", (id_entry.get().strip(),))
            conn.commit()
            messagebox.showinfo("Success", "Student deleted successfully.")
            clear_fields(id_entry, name_entry, birthdate_entry, phone_entry, email_entry, address_entry, treeview=treeview, check=True)
            treeview_data(treeview)
            return
        except Exception as e:
            messagebox.showerror("Error", f"Invalid operation due to: {e}")
        finally:
            conn.close()

def search_student(id: int) -> dict | None:
    """
    Search for a student record in the database by ID.

    This function queries the STUDENTS table for a matching student ID.
    If found, it returns the student record as a tuple; otherwise, it
    returns None. Displays error messages if the search term is missing
    or if a database error occurs.

    Behavior
    --------
    - Shows an error if no ID is provided.
    - Executes a SQL SELECT statement to find the student.
    - Returns the first matching record as a tuple, or None if not found.
    - Displays an error message if a database exception occurs.
    - Ensures the database connection is closed in a `finally` block.
    """
    if not id:
        messagebox.showerror("Error", "Please enter a search term.")
        return
    try:
        conn, cursor = connect_database()
        cursor.execute("SELECT * FROM STUDENTS WHERE id = %s", (id,))
        result = cursor.fetchone()
        if result:
            return result
        else:
            return None
    except Exception as e:
        messagebox.showerror("Error", f"Invalid operation due to: {e}")
    finally:
        conn.close()

def search_bar(search_combobox: ttk.Combobox, search_entry: Entry, treeview: ttk.Treeview) -> None:
    """
    Perform a student search based on the selected criteria and update the Treeview.

    This function checks the search term and selected option (ID or Name),
    queries the STUDENTS table accordingly, and refreshes the Treeview with
    the matching results. Displays warnings or errors if the input is invalid
    or if a database exception occurs.

    Behavior
    --------
    - Shows a warning if no search term is entered.
    - Shows a warning if no valid search option is selected.
    - Executes a SQL SELECT statement based on the chosen option (ID or Name).
    - Clears the Treeview and repopulates it with the query results.

    Notes
    -----
    - Only supports searching by ID or Name.
    - Results are inserted into the Treeview with columns: id, name, birthdate,
      phone, email, address, total_penalty.
    """

    if not search_entry:
        messagebox.showwarning("Error", "Please enter a search term.")
        return

    if search_combobox == "Search by":
        messagebox.showwarning("Invalid Selection", "Please select an option.")
        return

    try:
        conn, cursor = connect_database()

        if search_combobox == "Id":
            cursor.execute("SELECT * FROM STUDENTS WHERE id = %s", (search_entry,))
        elif search_combobox == "Name":
            cursor.execute("SELECT * FROM STUDENTS WHERE name = %s", (search_entry,))
        else:
            messagebox.showwarning("Invalid Selection", "Unsupported search option.")
            return

        results = cursor.fetchall()
        treeview.delete(*treeview.get_children())

        for row in results:
            treeview.insert("", END, values=(
                row["id"], row["name"], row["birthdate"],
                row["phone"], row["email"], row["address"],
                row["total_penalty"]
            ))

    except Exception as e:
        messagebox.showerror("Error", f"Invalid operation due to: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

def select_student(event, treeview: ttk.Treeview = None, id_entry: Entry = None, name_entry: Entry = None, 
                   birthdate_entry: Entry = None, phone_entry: Entry = None, email_entry: Entry = None, address_entry: Entry = None):
    """
    Populate entry fields with data from the selected student in the Treeview.

    When a row is selected, this function retrieves its values and fills the
    corresponding entry widgets. If only `id_entry` is provided, then only the
    student ID field is updated. Otherwise, all provided fields are cleared and
    repopulated with the row data.

    Notes
    -----
    - Calls `clear_fields(...)` before repopulating entries.
    - Student ID is disabled after being inserted.
    - Phone number is zero-padded to ensure 11 digits.
    """
    # Stores the given values of the selected row
    index = treeview.selection()
    if not index:
        return
    item_id = index[0]
    content = treeview.item(item_id)
    row = content['values']

    # Popupalte only id_entry for other forms
    if name_entry is None:
        id_entry.delete(0, END)
        id_entry.insert(0, row[0])
        return
    
    # Clear entry fields and populates with new entries

    clear_fields(id_entry, name_entry, birthdate_entry,
                 phone_entry, email_entry, address_entry, treeview=treeview, check=False)
    id_entry.insert(0, row[0])
    id_entry.config(state='disabled')
    name_entry.insert(0, row[1])
    birthdate_entry.insert(0, row[2])
    phone_str = str(row[3]).zfill(11)   
    phone_entry.insert(0, phone_str)
    email_entry.insert(0, row[4])
    address_entry.insert(0, row[5])

def clear_fields(*entries, treeview: ttk.Treeview = None, check: bool):
    """
    Reset the given entry or text widgets and optionally clear Treeview selection.

    This function restores entry widgets to a normal state, deletes their content,
    and handles both `Entry` and `Text` widgets safely. If `check` is True and a
    Treeview is provided, the current selection in the Treeview is also removed.

    Behavior
    --------
    - Ignores None values in the entries list.
    - Restores each widget's state to "normal" before clearing.
    - Deletes content using the appropriate method for `Entry` or `Text`.
    - Silently skips widgets that raise `TclError`.
    - Optionally clears Treeview selection when `check` is True.
    """
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
