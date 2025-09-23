from tkinter import *
from tkinter import ttk
from datetime import datetime

def book_form():
    global backbutton_image

    books_frame = Frame(root,bg="white", bd=2, relief=RIDGE)
    books_frame.place(x=205, y= 98, relheight=1, width=1000)
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

    search_button = Button(searchFrame, text="SEARCH", font=('times new roman', 12), bg="#2b7192", fg="white", width=10, cursor="hand2")
    search_button.grid(row=0, column=2, padx=20)

    showall_button = Button(searchFrame, text="Show All", font=('times new roman', 12), bg="#2b7192", fg="white", width=10, cursor="hand2")
    showall_button.grid(row=0, column=3)

    vertical_scrollbar = Scrollbar(top_frame, orient=VERTICAL)
    book_treeview = ttk.Treeview(top_frame, columns=("title", "author", "quantity"), show="headings", yscrollcommand=vertical_scrollbar.set)
    vertical_scrollbar.pack(side=RIGHT, fill=Y, pady=(10,0))
    vertical_scrollbar.config(command=book_treeview.yview)
    book_treeview.pack(pady=(10, 0), fill=BOTH)
    book_treeview.heading("title", text="Title")
    book_treeview.heading("author", text="Author")
    book_treeview.heading("quantity", text="Quantity")

    book_treeview.column("title", width=200)
    book_treeview.column("author", width=140)
    book_treeview.column('quantity', width=60)
    # End of top frame

    # Start of middle frame
    middle_frame = Frame(books_frame, bg ="white")
    middle_frame.pack(fill=X)

    b_title= Label(middle_frame, text= "Title", font=("times new roman", 12), bg="white", fg="black",)
    b_title.grid(row=0, column=0)
    b_title_entry = Entry(middle_frame, font=("times new roman", 12), bg="white")
    b_title_entry.grid(row=0, column=1, padx=20, pady=10)

    b_author = Label(middle_frame, text="Author", font=("times new roman", 12), bg="white", fg="black")
    b_author.grid(row=1, column=0)
    b_author_entry = Entry(middle_frame, font=("times new roman", 12), bg="white")
    b_author_entry.grid(row=1, column=1, padx=20, pady=10)

    b_quantity = Label(middle_frame, text="Quantity", font=("times new roman", 12), bg="white", fg="black")
    b_quantity.grid(row=2, column=0)
    b_quantity_entry = Entry(middle_frame, font=("times new roman", 12), bg="white")
    b_quantity_entry.grid(row=2, column=1, padx=20, pady=10)

    b_year = Label(middle_frame, text="Publication Year", font=("times new roman", 12), bg="white", fg="black")
    b_year.grid(row=3, column=0)
    current_year = datetime.now().year
    year_list = [i for i in range(1800, current_year + 1)]
    b_year_combobox = ttk.Combobox(middle_frame, values=year_list, font=("times new roman", 12), width= 18, state="read only")
    b_year_combobox.grid(row=3, column=1, padx=20, pady=10)

    b_edition = Label(middle_frame, text="Edition", font=("times new roman", 12), bg="white", fg="black")
    b_edition.grid(row=0, column=2)
    b_edition_entry = Entry(middle_frame, font=("times new roman", 12), bg="light gray")
    b_edition_entry.grid(row=0, column=3, padx=20, pady=10)
    make_optional(b_edition_entry)

    b_language = Label(middle_frame, text="Language", font=("times new roman", 12), bg="white", fg="black")
    b_language.grid(row=1, column=2)
    b_language_entry = Entry(middle_frame, font=("times new roman", 12), bg="light gray")
    b_language_entry.grid(row=1, column=3, padx=20, pady=10)
    make_optional(b_language_entry)
    # End of middle frame

    # Start of bottom frame
    bottom_frame = Frame(books_frame, bg="white")
    bottom_frame.pack(anchor="s")

    save_btn = Button(bottom_frame, text="Save", font=("times new roman", 12, "bold"), fg="white", bg="#00566b", cursor="hand2")
    save_btn.grid(row=0, column=0, padx= 25)

    update_btn = Button(bottom_frame, text="Update", font=("times new roman", 12, "bold"), fg="white", bg="#00566b", cursor="hand2")
    update_btn.grid(row=0, column=1, padx= 25)

    delete_btn = Button(bottom_frame, text="Delete", font=("times new roman", 12, "bold"), fg="white", bg="#00566b", cursor="hand2")
    delete_btn.grid(row=0, column=2, padx= 25)


def mark_optional_on_focus_in(event):
    event.widget.config(bg="white")

def restore_optional_on_focus_out(event):
    if not event.widget.get():
        event.widget.config(bg="light gray")

def make_optional(entry_widget):
    entry_widget.bind("<FocusIn>", mark_optional_on_focus_in)
    entry_widget.bind("<FocusOut>", restore_optional_on_focus_out)

# Main window
root = Tk()

root.title("Libray Management System")
root.geometry("1270x680+40+10")
root.resizable(0, 0)
root.configure(bg="#f0f9ff")

bg_image = PhotoImage(file="images\\library.png")
title_frame = Frame(root, bg="#010c48")
title_frame.pack(fill=X)
titleLabel = Label(title_frame, image=bg_image, compound=LEFT, text="Library Management System  ", font=("times new roman", 40, 'bold'), bg="#010c48", fg="white", anchor='w', padx=20)
titleLabel.pack(side=LEFT)

logoutButton = Button(title_frame, text="Logout", font=("times new roman", 15, 'bold'), fg="white", bg="#00566b", cursor="hand2")
logoutButton.pack(side=RIGHT, padx=(0,10))

subtitleLabel = Label(root, text="Welcome to Library Management System\t Date: 2025-01-01\t\t\tTime: 12:00 PM", font=("times new roman", 15), bg="#8A97D9", fg="white")
subtitleLabel.pack(fill=X)

# Star of left menu
leftFrame = Frame(root, bg="#f0f9ff")
leftFrame.pack(fill=Y, side=LEFT)

logo_Image = PhotoImage(file="images\\digital-library.png")
imageLabel = Label(leftFrame, image=logo_Image, bg="#f0f9ff")
imageLabel.pack()

menuLabel = Label(leftFrame, text="Menu", font=("times new roman", 20, "bold"), bg="#048B85", fg="black")
menuLabel.pack(fill=X)

book_icon = PhotoImage(file="images\\book.png")
BookButton = Button(leftFrame, image=book_icon, compound=LEFT, text="  Books", font=("times new roman", 20, 'bold'), bg="white", fg="black", cursor="hand2", anchor='w', padx=12, command=book_form)
BookButton.pack(fill=X)

student_icon = PhotoImage(file="images\\student.png")
StudentButton = Button(leftFrame, image=student_icon, compound=LEFT, text="  Students", font=("times new roman", 20, 'bold'), bg="white", fg="black", cursor="hand2", anchor='w', padx=12)
StudentButton.pack(fill=X)

borrow_icon = PhotoImage(file="images\\borrow.png")
BorrowButton = Button(leftFrame, image=borrow_icon, compound=LEFT, text="  Loans", font=("times new roman", 20, 'bold'), bg="white", fg="black", cursor="hand2", anchor='w', padx=12)
BorrowButton.pack(fill=X)

penalty_icon = PhotoImage(file="images\\warning.png")
PenaltyButton = Button(leftFrame, image=penalty_icon, compound=LEFT, text="  Penalties", font=("times new roman", 20, 'bold'), bg="white", fg="black", cursor="hand2", anchor='w', padx=12)
PenaltyButton.pack(fill=X)

exit_icon = PhotoImage(file="images\\exit.png")
ExitButton = Button(leftFrame, image=exit_icon, compound=LEFT, text="  Exit", font=("times new roman", 20, 'bold'), bg="white", fg="black", cursor="hand2", command=root.quit, anchor='w', padx=12)
ExitButton.pack(fill=X)
# End of left menu

# Start of flashcards frame
flash_card_frame = Frame(root)
flash_card_frame.pack(fill=BOTH)

# Display total books flash card
book_frame = Frame(flash_card_frame, bg="#343B64", bd=3, relief=RIDGE)
book_frame.pack(fill=X)


bookshelf_icon = PhotoImage(file="images\\bookshelf.png")
bookshelfLabel = Label(book_frame, image=bookshelf_icon, bg="#343B64")
bookshelfLabel.pack(pady=10)
total_books_label = Label(book_frame, text="Total Books", font=("times new roman", 20, 'bold'), bg="#343B64", fg="white")
total_books_label.pack()
total_books_count = Label(book_frame, text="150", font=("times new roman", 20, 'bold'), bg="#343B64", fg="white")
total_books_count.pack()

# Diplay total students flash card
student_frame = Frame(flash_card_frame, bg="#11523C", bd=3, relief=RIDGE)
student_frame.pack(fill=X)   

students_icon = PhotoImage(file="images\\group.png")
studentsLabel = Label(student_frame, image=students_icon, bg="#11523C")
studentsLabel.pack(pady=10)
total_students_label = Label(student_frame, text="Total Students", font=("times new roman", 20, 'bold'), bg="#11523C", fg="white")
total_students_label.pack()
total_students_count = Label(student_frame, text="120", font=("times new roman", 20, 'bold'), bg="#11523C", fg="white")
total_students_count.pack()

# Display active loans flash card
loan_frame = Frame(flash_card_frame, bg="#7A4A91", bd=3, relief=RIDGE)
loan_frame.pack(fill=X)

loan_icon = PhotoImage(file="images\\borrowed_book.png")
loanLabel = Label(loan_frame, image=loan_icon, bg="#7A4A91")
loanLabel.pack(pady=10)
total_loan_label = Label(loan_frame, text="Active Loans", font=("times new roman", 20, 'bold'), bg="#7A4A91", fg="white")
total_loan_label.pack()
total_loan_count = Label(loan_frame, text="53", font=("times new roman", 20, 'bold'), bg="#7A4A91", fg="white")
total_loan_count.pack()
# End of flashcards frame


root.mainloop() 

