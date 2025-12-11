from database import connect_database
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from tkinter import *
from books import make_optional
from datetime import datetime 
import re

def treeview_data():
    global student_treeview
    try:
        conn, cursor = connect_database()
        cursor.execute("SELECT * FROM STUDENTS")
        results = cursor.fetchall()
        student_treeview.delete(*student_treeview.get_children())
        for row in results:
            student_treeview.insert("", END, values=(
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

def student_form(root): 
    global student_treeview, backbutton_image

    students_frame = Frame(root,bg="white", bd=2, relief=RIDGE)
    students_frame.place(x=205, y= 98, relheight=1, width=1065)
    header = Label(students_frame, text="Student Management", font=("times new roman", 15, 'bold'), bg="#2b7192", fg="white", anchor='center')
    header.pack(fill=X)

    backbutton_image = PhotoImage(file="images\\return.png")
    back_button = Button(students_frame, image=backbutton_image, cursor="hand2", bg="#2b7192",bd=0 , command=lambda: students_frame.destroy())
    back_button.place(x=5, y=0)

   # Start of top frame
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
                           cursor="hand2", command=lambda: search_bar(search_combobox.get(), search_entry.get()))
    search_button.grid(row=0, column=2, padx=20)

    showall_button = Button(searchFrame, text="Show All", font=('times new roman', 12), bg="#2b7192", fg="white", width=10, 
                            cursor="hand2", command=lambda: treeview_data())
    showall_button.grid(row=0, column=3)

    vertical_scrollbar = Scrollbar(top_frame, orient=VERTICAL)
    student_treeview = ttk.Treeview(top_frame, columns=("id", "name", "birthdate", "phone", "email", "address", "total_penalty"), show="headings", yscrollcommand=vertical_scrollbar.set)
    vertical_scrollbar.pack(side=RIGHT, fill=Y, pady=(10,0))
    vertical_scrollbar.config(command=student_treeview.yview)
    student_treeview.pack(pady=(10, 0), fill=BOTH, expand=TRUE)
    student_treeview.heading("id", text="Id", anchor="w")
    student_treeview.heading("name", text="Name", anchor="w")
    student_treeview.heading("birthdate", text="Birthdate", anchor="w")
    student_treeview.heading("phone", text="Phone", anchor="w")
    student_treeview.heading("email", text="Email", anchor="w")
    student_treeview.heading("address", text="Address", anchor="w")
    student_treeview.heading("total_penalty", text="Penalties", anchor="w")

    student_treeview.column("id", width=25, anchor="w")
    student_treeview.column("name", width=200, anchor="w")
    student_treeview.column("birthdate", width=80, anchor="w")
    student_treeview.column("phone", width=80, anchor="w")
    student_treeview.column("email", width=100, anchor="w")
    student_treeview.column("address", width=120, anchor="w")
    student_treeview.column("total_penalty", width=5, anchor="w")

    treeview_data()
    # End of top frame

    # Start of bottom frame
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

    student_treeview.bind("<ButtonRelease-1>", lambda event: select_student(event, s_id_entry, s_name_entry, s_birthdate_entry,
                                                                        s_phone_entry, s_email_entry, s_address_entry))

    add_btn = Button(bottom_frame, text="Add", font=("times new roman", 12, "bold"), width= 15, fg="white", 
        bg="#00566b", cursor="hand2", command=lambda: add_student(s_id_entry, s_name_entry, s_birthdate_entry,
                                                                   s_phone_entry, s_email_entry, s_address_entry))
    add_btn.grid(row=4, column=0, padx=0, pady=20)

    update_btn = Button(bottom_frame, text="Update", font=("times new roman", 12, "bold"), width= 15, fg="white",
        bg="#00566b",cursor="hand2", command=lambda: update_student(s_id_entry, s_name_entry, 
                                                                          s_birthdate_entry, s_phone_entry, s_email_entry, 
                                                                          s_address_entry))
    update_btn.grid(row=4, column=1, padx=(20,0), pady=20)

    delete_btn = Button(bottom_frame,text="Delete",font=("times new roman", 12, "bold"), width= 15, fg="white",
        bg="#00566b", cursor="hand2", command=lambda: delete_student(s_id_entry, s_name_entry, s_birthdate_entry,
                                                                     s_phone_entry, s_email_entry, s_address_entry))
    delete_btn.grid(row=4, column=2, padx=(20,0), pady=20)

    clear_btn = Button(bottom_frame, text="Clear", font=("times new roman", 12, "bold"), width= 15, fg="white",
        bg="#00566b", cursor="hand2", command=lambda: clear_fields(s_id_entry, s_name_entry, s_birthdate_entry,
                                                                   s_phone_entry, s_email_entry, s_address_entry, True))
    clear_btn.grid(row=4, column=3, padx=(20,0), pady=20)
    # End of bottom frame


def add_student(id_entry, name_entry, birthdate_entry, phone_entry, email_entry, address_entry):
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
        treeview_data()
        clear_fields(id_entry, name_entry, birthdate_entry, phone_entry, email_entry, address_entry, True)
        messagebox.showinfo("Success", "Student added successfully.")
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

def update_student(id_entry, name_entry, birthdate_entry, phone_entry, email_entry, address_entry):
    index = student_treeview.selection()
    content = student_treeview.item(index)
    row = content["values"]
    id = row[0]

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
            name_entry.get(), birthdate_entry.get(), phone_entry.get(), email_entry.get(), address_entry.get(), id))
        conn.commit()
        messagebox.showinfo("Success", "Student updated successfully.")
        clear_fields(id_entry, name_entry, birthdate_entry, phone_entry, email_entry, address_entry, True)
        treeview_data()
        return
    except Exception as e:
        messagebox.showerror("Error", f"Invalid operation due to: {e}")
    finally:
        conn.close()

def delete_student(id_entry, name_entry, birthdate_entry, phone_entry, email_entry, address_entry):
    index = student_treeview.selection()
    content = student_treeview.item(index)
    row = content["values"]
    id = row[0]
    result = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this student?")
    if result:
        try: 
            conn, cursor = connect_database()
            cursor.execute("DELETE FROM STUDENTS WHERE id=%s", (id,))
            conn.commit()
            messagebox.showinfo("Success", "Student deleted successfully.")
            clear_fields(id_entry, name_entry, birthdate_entry, phone_entry, email_entry, address_entry, True)
            treeview_data()
            return
        except Exception as e:
            messagebox.showerror("Error", f"Invalid operation due to: {e}")
        finally:
            conn.close()

def search_student(id):
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

def search_bar(search_combobox, search_entry):
    global student_treeview
    if not search_entry:
        messagebox.showerror("Error", "Please enter a search term.")
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
        student_treeview.delete(*student_treeview.get_children())

        for row in results:
            student_treeview.insert("", END, values=(
                row["id"], row["name"], row["birthdate"],
                row["phone"], row["email"], row["address"],
                row["total_penalty"]
            ))

    except Exception as e:
        messagebox.showerror("Error", f"Invalid operation due to: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

def clear_fields(id, name, birthdate, phone, email, address, check):
    id.config(state='normal')
    id.delete(0, END)
    name.delete(0, END)
    phone.delete(0, END)
    email.delete(0, END)
    address.delete(0, END)
    birthdate.delete(0, END)
    if check:
        student_treeview.selection_remove(student_treeview.selection())

def select_student(event, id_entry, name_entry, birthdate_entry,
                   phone_entry, email_entry, address_entry):
    index = student_treeview.selection()
    if not index:
        return
    item_id = index[0]
    content = student_treeview.item(item_id)
    row = content['values']

    clear_fields(id_entry, name_entry, birthdate_entry,
                 phone_entry, email_entry, address_entry, False)
    id_entry.insert(0, row[0])
    id_entry.config(state='disabled')
    name_entry.insert(0, row[1])
    birthdate_entry.insert(0, row[2])
    phone_str = str(row[3]).zfill(11)   
    phone_entry.insert(0, phone_str)
    email_entry.insert(0, row[4])
    address_entry.insert(0, row[5])
