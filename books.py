from database import connect_database
from tkinter import messagebox, ttk
from tkinter import *
from datetime import datetime 

def treeview_data():
    global book_treeview
    try:
        conn, cursor = connect_database()
        cursor.execute("SELECT * FROM books")
        results = cursor.fetchall()
        book_treeview.delete(*book_treeview.get_children())
        for row in results:
            book_treeview.insert("", END, values=(
                row["id"],
                row["title"],
                row["author"],
                row["quantity"],
                row["year"],
                row["edition"],
                row["language"]
            ))
    except Exception as e:
        return e
    finally:
        conn.close()

def create_book_treeview(parent_frame):
    global book_treeview

    vertical_scrollbar = Scrollbar(parent_frame, orient=VERTICAL)
    book_treeview = ttk.Treeview(parent_frame, columns=("id", "title", "author", "quantity", "year", "edition", "language"), show="headings", yscrollcommand=vertical_scrollbar.set)
    vertical_scrollbar.pack(side=RIGHT, fill=Y, pady=(10,0))
    vertical_scrollbar.config(command=book_treeview.yview)
    book_treeview.heading("id", text="Id", anchor="w")
    book_treeview.heading("title", text="Title", anchor="w")
    book_treeview.heading("author", text="Author", anchor="w")
    book_treeview.heading("quantity", text="Quantity", anchor="w")
    book_treeview.heading("year", text="Year", anchor="w")
    book_treeview.heading("edition", text="Edition", anchor="w")
    book_treeview.heading("language", text="Language", anchor="w")

    book_treeview.column("id", width=20, anchor="w")
    book_treeview.column("title", width=200, anchor="w")
    book_treeview.column("author", width=140, anchor="w")
    book_treeview.column("quantity", width=60, anchor="w")
    book_treeview.column("year", width=60, anchor="w")
    book_treeview.column("edition", width=60, anchor="w")
    book_treeview.column("language", width=100, anchor="w")

    treeview_data()
    return book_treeview

def book_form(root):
    global backbutton_image, book_treeview

    books_frame = Frame(root,bg="white", bd=2, relief=RIDGE)
    books_frame.place(x=205, y= 98, relheight=1, width=1065)
    header = Label(books_frame, text="Book Management", font=("times new roman", 15, 'bold'), bg="#2b7192", fg="white", anchor='center')
    header.pack(fill=X)

    backbutton_image = PhotoImage(file="images\\return.png")
    back_button = Button(books_frame, image=backbutton_image, cursor="hand2", bg="#2b7192",bd=0 , command=lambda: books_frame.destroy())
    back_button.place(x=5, y=0)

    # Start of top frame
    top_frame = Frame(books_frame, bg="#f0f9ff")
    top_frame.pack(fill=X)

    searchFrame = Frame(top_frame, bg="#f0f9ff")
    searchFrame.pack()
    search_combobox = ttk.Combobox(searchFrame, values=("Title","Author"), font=("times new roman", 12), state="readonly", justify="center")
    search_combobox.set("Search by")
    search_combobox.grid(row=0, column=0, padx= 20)
    search_entry = Entry(searchFrame,font=("times new roman", 12), bg="light gray")
    search_entry.grid(row=0, column=1)
    make_optional(search_entry)

    search_button = Button(searchFrame, text="SEARCH", font=('times new roman', 12), bg="#2b7192", fg="white", width=10,
                           cursor="hand2", command=lambda: search_book_title_author(search_combobox.get(), search_entry.get()))
    search_button.grid(row=0, column=2, padx=20)

    showall_button = Button(searchFrame, text="Show All", font=('times new roman', 12), bg="#2b7192", fg="white", width=10, 
                            cursor="hand2", command=lambda: treeview_data())
    showall_button.grid(row=0, column=3)

    book_treeview = create_book_treeview(top_frame)
    book_treeview.pack(pady=(10, 0), fill=BOTH)
    
    treeview_data()
    # End of top frame

    # Start of bottom frame
    bottom_frame = Frame(books_frame, bg ="white")
    bottom_frame.pack(anchor=CENTER)

    b_title= Label(bottom_frame, text= "Title", font=("times new roman", 12), bg="white", fg="black",)
    b_title.grid(row=0, column=0)
    b_title_entry = Entry(bottom_frame, font=("times new roman", 12), bg="white")
    b_title_entry.grid(row=0, column=1, padx=20, pady=10)

    b_author = Label(bottom_frame, text="Author", font=("times new roman", 12), bg="white", fg="black")
    b_author.grid(row=1, column=0)
    b_author_entry = Entry(bottom_frame, font=("times new roman", 12), bg="white")
    b_author_entry.grid(row=1, column=1, padx=20, pady=10)

    b_quantity = Label(bottom_frame, text="Quantity", font=("times new roman", 12), bg="white", fg="black")
    b_quantity.grid(row=2, column=0)
    b_quantity_entry = Entry(bottom_frame, font=("times new roman", 12), bg="white")
    b_quantity_entry.grid(row=2, column=1, padx=20, pady=10)

    b_year = Label(bottom_frame, text="Publication Year", font=("times new roman", 12), bg="white", fg="black")
    b_year.grid(row=0, column=2)
    current_year = datetime.now().year
    year_list = [i for i in range(1800, current_year + 1)]
    b_year_combobox = ttk.Combobox(bottom_frame, values=year_list, font=("times new roman", 12), width= 18, state="readonly")
    b_year_combobox.grid(row=0, column=3, padx=20, pady=10)

    b_edition = Label(bottom_frame, text="Edition", font=("times new roman", 12), bg="white", fg="black")
    b_edition.grid(row=1, column=2)
    b_edition_entry = Entry(bottom_frame, font=("times new roman", 12), bg="light gray")
    b_edition_entry.grid(row=1, column=3, padx=20, pady=10)
    make_optional(b_edition_entry)
    
    b_language = Label(bottom_frame, text="Language", font=("times new roman", 12), bg="white", fg="black")
    b_language.grid(row=2, column=2)
    b_language_entry = Entry(bottom_frame, font=("times new roman", 12), bg="white")
    b_language_entry.grid(row=2, column=3, padx=20, pady=10)

    book_treeview.bind("<ButtonRelease-1>", lambda event: select_data(event, b_title_entry, b_author_entry,
                                                        b_quantity_entry, b_year_combobox,
                                                        b_language_entry, b_edition_entry)) 

    add_btn = Button(bottom_frame, text="Add", font=("times new roman", 12, "bold"), width= 15, fg="white", 
        bg="#00566b", cursor="hand2", command=lambda: add_book(b_title_entry, b_author_entry,
                                                                 b_quantity_entry, b_year_combobox, 
                                                                 b_language_entry, b_edition_entry))
    add_btn.grid(row=4, column=0, padx=0, pady=20)

    update_btn = Button(bottom_frame, text="Update", font=("times new roman", 12, "bold"), width= 15, fg="white",
        bg="#00566b",cursor="hand2", command=lambda: update_data(b_title_entry, b_author_entry,
                                                                 b_quantity_entry, b_year_combobox, 
                                                                 b_language_entry, b_edition_entry))
    update_btn.grid(row=4, column=1, padx=10, pady=20)

    delete_btn = Button(bottom_frame,text="Delete",font=("times new roman", 12, "bold"), width= 15, fg="white",
        bg="#00566b", cursor="hand2", command=lambda: delete_data(b_title_entry, b_author_entry,
                                                                     b_quantity_entry, b_year_combobox,
                                                                     b_language_entry, b_edition_entry))
    delete_btn.grid(row=4, column=2, padx=10, pady=20)

    clear_btn = Button(bottom_frame, text="Clear", font=("times new roman", 12, "bold"), width= 15, fg="white",
        bg="#00566b", cursor="hand2", command=lambda: clear_fields(b_title_entry, b_author_entry,
                                                                     b_quantity_entry, b_year_combobox,
                                                                     b_language_entry, b_edition_entry, True))
    clear_btn.grid(row=4, column=3, padx=10, pady=20)
    # End of bottom frame
    

def add_book(title_entry, author_entry, quantity_entry, year_entry, language_entry, edition_entry=""):
    title = title_entry.get()
    author = author_entry.get()
    quantity = quantity_entry.get()
    year = year_entry.get()
    language = language_entry.get()
    edition = edition_entry.get()

    if not (title and author and quantity and year and language):
        messagebox.showerror("Incomplete Info", "Please complete all required fields.")
        return
    try:
        quantity = int(quantity)
    except ValueError:
        messagebox.showerror("Invalid input", "Quantity must be numeric.")
        return

    conn, cursor = connect_database()
    try:
        if search_book(title, author, language, edition):
            messagebox.showinfo("Duplicate Entry", "This book already exists in the database.")
            return 

        cursor.execute(
            "INSERT INTO BOOKS (title, author, quantity, year, edition, language) VALUES (%s, %s, %s, %s, %s, %s)",
            (title.strip(), author.strip(), quantity, year, edition.strip(), language.strip())
        )
        conn.commit()
        treeview_data()
        clear_fields(title_entry, author_entry, quantity_entry, year_entry, language_entry, edition_entry, True)
        messagebox.showinfo("Success", "Book inserted successfully")
        return True

    except Exception as e:
        messagebox.showerror("Error", str(e))
        return e

    finally:
        conn.close()

def clear_fields(title_entry, author_entry, quantity_entry, year_entry, 
                 language_entry, edition_entry, check):
    title_entry.delete(0, END)
    author_entry.delete(0, END)
    quantity_entry.delete(0, END)
    year_entry.set("")    
    language_entry.delete(0, END)
    edition_entry.delete(0, END)
    if check:
        book_treeview.selection_remove(book_treeview.selection())
    

def select_data(event, title_entry, author_entry=None, quantity_entry=None, year_combobox=None, 
                language_entry=None, edition_entry=None):
    index = book_treeview.selection()
    if not index:
        return
    content = book_treeview.item(index)
    row = content["values"]
    if author_entry is None:
        title_entry.delete(0, END)
        title_entry.insert(0, row[1])
        return
    clear_fields(title_entry, author_entry, quantity_entry, year_combobox, 
                 edition_entry, language_entry, False)
    title_entry.insert(0, row[1])
    author_entry.insert(0, row[2])
    quantity_entry.insert(0, row[3])
    year_combobox.set(row[4])
    language_entry.insert(0, row[6])
    edition_entry.insert(0, row[5])    

def update_data(title_entry, author_entry, quantity_entry, year_combobox, 
                language_entry, edition_entry):
    index = book_treeview.selection()
    content = book_treeview.item(index)
    row = content["values"]
    id = row[0]
    
    try: 
        conn, cursor = connect_database()
        cursor.execute("UPDATE BOOKS SET title = %s, author = %s, quantity = %s, " \
        "year = %s, language = %s, edition = %s WHERE id = %s", (title_entry.get(), author_entry.get(), quantity_entry.get(),
                                                                 year_combobox.get(), language_entry.get(), edition_entry.get(), id))
        conn.commit()
        messagebox.showinfo("Book Updated", "Book has been updated sucesfully.")
        clear_fields(title_entry, author_entry, quantity_entry, year_combobox, 
                 edition_entry, language_entry, True)
        treeview_data()
        return
    except Exception as e:
        messagebox.showerror("Error", f"Invalid operation due to {e}")
        return
    finally:
        conn.close()

def delete_data(title_entry, author_entry, quantity_entry, year_combobox, 
                language_entry, edition_entry):
    index = book_treeview.selection()
    content = book_treeview.item(index)
    row = content["values"]
    id = row[0]
    result = messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete this book?", icon='warning')
    if result:
        try: 
            conn, cursor = connect_database()
            cursor.execute("DELETE FROM BOOKS WHERE id = %s", (id,))
            conn.commit()
            messagebox.showinfo("Book Deleted", "Book has been deleted sucesfully.")
            clear_fields(title_entry, author_entry, quantity_entry, year_combobox, 
                    language_entry, edition_entry, True)
            treeview_data()
            return
        except Exception as e:
            messagebox.showerror("Error", f"Invalid operation due to: {e}")
            return
        finally:
            conn.close()

def search_book(title, author="", language="", edition=""):
    conn, cursor = connect_database() 
    if author == "":
        try:
            cursor.execute("SELECT * FROM BOOKS WHERE title = %s", (title,))
            result = cursor.fetchone()
            return dict(result) if result else None
        except Exception as e:
            return e
        finally:
            if conn:
                conn.close()
    try:
        cursor.execute("SELECT * FROM BOOKS WHERE title = %s and author = %s and language = %s and edition = %s", 
                       (title, author, language, edition))
        result = cursor.fetchone()
        return dict(result) if result else None
    except Exception as e: 
        return e
    finally:
        if conn:
            conn.close()

def search_book_title_author(search_combobox, search_entry):
    global book_treeview
    if not search_entry:
        messagebox.showerror("Validation Error", "Search field must be filled out.")
        return
    conn, cursor = connect_database()
    if search_combobox == "Search by":
        messagebox.showwarning("Invalid Selection", "Search cannot proceed without a selected option.")
        return
    elif search_combobox == "Title":
        try:
            cursor.execute("SELECT * FROM BOOKS WHERE title = %s", (search_entry,))
            results = cursor.fetchall()
            book_treeview.delete(*book_treeview.get_children())
            for row in results:
                book_treeview.insert("", END, values=(
                    row["id"],
                    row["title"],
                    row["author"],
                    row["quantity"],
                    row["year"],
                    row["edition"],
                    row["language"]
                ))
            return                
        except Exception as e:
            messagebox.showerror("Error", f"Invalid operation due to: {e}")
        finally:
            conn.close()
    else:
        try:
            cursor.execute("SELECT * FROM BOOKS WHERE author = %s", (search_entry,))
            results = cursor.fetchall()
            book_treeview.delete(*book_treeview.get_children())
            for row in results:
                book_treeview.insert("", END, values=(
                    row["id"],
                    row["title"],
                    row["author"],
                    row["quantity"],
                    row["year"],
                    row["edition"],
                    row["language"]
                ))
            return
        except Exception as e:
            messagebox.showerror("Error", f"Invalid operation due to: {e}")
        finally:
            conn.close()

def search_book_id(id):
    try:
        conn, cursor = connect_database()
        cursor.execute("SELECT * FROM BOOKS WHERE id = %s", (id,))
        result = cursor.fetchone()
        return dict(result) if result else None
    except Exception as e:
        return e
    finally:
        if conn:
            conn.close()

def increase_book_quantity(title, edition, quantity=1):
    conn, cursor = connect_database()

    try:
        cursor.execute("SELECT quantity FROM BOOKS WHERE title = %s and edition = %s", (title, edition,))
        result = cursor.fetchone()

        new_quantity = result['quantity'] + quantity
        query = 'UPDATE BOOKS SET quantity = %s WHERE title = %s and edition = %s'
        cursor.execute(query, (new_quantity, title, edition,))
        conn.commit()
        return new_quantity
    except Exception as e:
        return e
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

def mark_optional_on_focus_in(event):
    event.widget.config(bg="white")

def restore_optional_on_focus_out(event):
    if not event.widget.get():
        event.widget.config(bg="light gray")

def make_optional(entry_widget):
    entry_widget.bind("<FocusIn>", mark_optional_on_focus_in)
    entry_widget.bind("<FocusOut>", restore_optional_on_focus_out)
