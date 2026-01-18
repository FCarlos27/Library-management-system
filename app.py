from tkinter import *
from books import book_form
from students import student_form
from loans import loans_form
from penalties import penalties_form
from login import login_form, logout
from database import initialize_database, connect_database
from datetime import datetime

initialize_database()
        
# Main window
root = Tk()
root.title("Libray Management System")
root.geometry("1270x680+40+10")
root.resizable(0, 0)
root.configure(bg="#f0f9ff")

def build_main_app(root: Tk) -> None:
    """
    This function creates the main app
    """

    # global vars for destroy_all()
    global leftFrame, title_frame, flash_card_frame

    # global var for update_time()
    global subtitleLabel

    # Global vars for flashcard_counts()
    global total_books_count, total_loan_count, total_students_count

    # Keep image references alive by attaching them to root
    root.bg_image = PhotoImage(file="images\\library.png")
    title_frame = Frame(root, bg="#010c48")
    title_frame.pack(fill=X)
    titleLabel = Label(
        title_frame,
        image=root.bg_image,
        compound=LEFT,
        text="Library Management System  ",
        font=("times new roman", 40, 'bold'),
        bg="#010c48",
        fg="white",
        anchor='w',
        padx=20
    )
    titleLabel.pack(side=LEFT)

    logoutButton = Button(
        title_frame,
        text="Logout",
        font=("times new roman", 15, 'bold'),
        fg="white",
        bg="#00566b",
        cursor="hand2", 
        command = lambda: [logout(root, build_main_app)]
    )
    logoutButton.pack(side=RIGHT, padx=(0,10))

    subtitleLabel = Label(root, text="", font=("times new roman", 15),
                          bg="#8A97D9", fg="white")
    subtitleLabel.pack(fill=X)

    # == Left Menu ==
    leftFrame = Frame(root, width=100, bg="#f0f9ff")
    leftFrame.pack(fill=Y, side=LEFT)

    root.logo_Image = PhotoImage(file="images\\librarian_resized.png")
    imageLabel = Label(leftFrame, image=root.logo_Image, bg="#f0f9ff")
    imageLabel.pack()

    menuLabel = Label(leftFrame, text="Menu", font=("times new roman", 20, "bold"),
                      bg="#048B85", fg="black")
    menuLabel.pack(fill=BOTH)

    root.book_icon = PhotoImage(file="images\\book.png")
    BookButton = Button(leftFrame, image=root.book_icon, compound=LEFT,
                        text="  Books", font=("times new roman", 20, 'bold'),
                        bg="white", fg="black", cursor="hand2", anchor='w', padx=12,
                        command=lambda: [destroy_all(root), book_form(root, flashcard_counts)])
    BookButton.pack(fill=X)

    root.student_icon = PhotoImage(file="images\\student.png")
    StudentButton = Button(leftFrame, image=root.student_icon, compound=LEFT,
                           text="  Students", font=("times new roman", 20, 'bold'),
                           bg="white", fg="black", cursor="hand2", anchor='w', padx=12,
                           command=lambda: [destroy_all(root), student_form(root, flashcard_counts)])
    StudentButton.pack(fill=X)

    root.borrow_icon = PhotoImage(file="images\\borrow.png")
    BorrowButton = Button(leftFrame, image=root.borrow_icon, compound=LEFT,
                          text="  Loans", font=("times new roman", 20, 'bold'),
                          bg="white", fg="black", cursor="hand2", anchor='w', padx=12,
                          command=lambda: [destroy_all(root), loans_form(root, flashcard_counts)])
    BorrowButton.pack(fill=X)

    root.penalty_icon = PhotoImage(file="images\\warning.png")
    PenaltyButton = Button(leftFrame, image=root.penalty_icon, compound=LEFT,
                           text="  Penalties", font=("times new roman", 20, 'bold'),
                           bg="white", fg="black", cursor="hand2", anchor='w', padx=12,
                           command=lambda: [destroy_all(root), penalties_form(root, flashcard_counts)])
    PenaltyButton.pack(fill=X)

    root.exit_icon = PhotoImage(file="images\\exit.png")
    ExitButton = Button(leftFrame, image=root.exit_icon, compound=LEFT,
                        text="  Exit", font=("times new roman", 20, 'bold'),
                        bg="white", fg="black", cursor="hand2", command=root.quit,
                        anchor='w', padx=12)
    ExitButton.pack(fill=X)

    # == Flashcards section ==
    flash_card_frame = Frame(root, bg="#f0f9ff")
    flash_card_frame.pack(fill=BOTH)

    # Display total books flash card
    book_frame = Frame(flash_card_frame, bg="#343B64", bd=3, relief=RIDGE, width=200)
    book_frame.grid(row=0, column=0, padx=250, pady=(15,0), ipadx=200)

    root.bookshelf_icon = PhotoImage(file="images\\bookshelf.png")
    bookshelfLabel = Label(book_frame, image=root.bookshelf_icon, bg="#343B64")
    bookshelfLabel.pack(pady=10)
    total_books_label = Label(book_frame, text="Total Books", font=("times new roman", 20, 'bold'),
                              bg="#343B64", fg="white")
    total_books_label.pack()
    total_books_count = Label(book_frame, text="150", font=("times new roman", 20, 'bold'),
                              bg="#343B64", fg="white")
    total_books_count.pack()

    # Display total students flash card
    student_frame = Frame(flash_card_frame, bg="#11523C", bd=3, relief=RIDGE)
    student_frame.grid(row=1, column=0, pady=5, ipadx=185)

    root.students_icon = PhotoImage(file="images\\group.png")
    studentsLabel = Label(student_frame, image=root.students_icon, bg="#11523C")
    studentsLabel.pack(pady=10)
    total_students_label = Label(student_frame, text="Total Students", font=("times new roman", 20, 'bold'),
                                 bg="#11523C", fg="white")
    total_students_label.pack()
    total_students_count = Label(student_frame, text="120", font=("times new roman", 20, 'bold'),
                                 bg="#11523C", fg="white")
    total_students_count.pack()

    # Display active loans flash card
    loan_frame = Frame(flash_card_frame, bg="#7A4A91", bd=3, relief=RIDGE)
    loan_frame.grid(row=2, column=0, ipadx=195)

    root.loan_icon = PhotoImage(file="images\\borrowed_book.png")
    loanLabel = Label(loan_frame, image=root.loan_icon, bg="#7A4A91")
    loanLabel.pack(pady=10)
    total_loan_label = Label(loan_frame, text="Active Loans", font=("times new roman", 20, 'bold'),
                             bg="#7A4A91", fg="white")
    total_loan_label.pack()
    total_loan_count = Label(loan_frame, text="53", font=("times new roman", 20, 'bold'),
                             bg="#7A4A91", fg="white")
    total_loan_count.pack()

    # Start updating after login
    update_time()
    flashcard_counts()

def destroy_all(root) -> None:
    """
    Destroy all child widgets of the given root except key frames and labels.

    This function iterates through all widgets inside the root window and
    removes them, preserving only the specified frames and labels that
    should remain visible (leftFrame, title_frame, subtitleLabel, flash_card_frame).
    """
    global leftFrame, title_frame, subtitleLabel, flash_card_frame

    for widget in root.winfo_children():
        if widget not in (leftFrame, title_frame, subtitleLabel,
                         flash_card_frame):
            widget.destroy()

def update_time() -> None:
    """
    Update the subtitle label with the current date and time.

    This function retrieves the current system date and time, formats them,
    and updates the subtitle label text. It reschedules itself to run every
    second to keep the display current.
    """
    global subtitleLabel

    # Get current date and time
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%I:%M:%S %p")  # 12-hour format with AM/PM

    # Update label text
    subtitleLabel.config(
        text=f"Welcome to Library Management System\t Date: {date_str}\t\t\tTime: {time_str}"
    )

    # Schedule next update after 1000 ms (1 second)
    subtitleLabel.after(1000, update_time)

def flashcard_counts():
    """
    Fetch and display counts for books, students, and active loans.

    This function queries the database for totals of books, students,
    and active loans, then updates the corresponding flashcard labels
    in the GUI. Returns an exception if a database error occurs.
    """
    global total_books_count, total_students, total_loan_count

    try:
        conn, cursor = connect_database()
        cursor.execute("SELECT COUNT(*) AS total FROM BOOKS")
        total_books = cursor.fetchone()['total']

        cursor.execute("SELECT COUNT(*) AS total FROM STUDENTS")
        total_students = cursor.fetchone()['total']

        cursor.execute("SELECT COUNT(*) AS total FROM LOANS WHERE status='active'")
        active_loans = cursor.fetchone()['total']
    except Exception as e:
        return e
    finally: 
        if conn:
            conn.close()

    total_books_count.config(text=str(total_books))
    total_students_count.config(text=str(total_students))
    total_loan_count.config(text=str(active_loans))

# Start updating
login_form(root, on_success=build_main_app)

root.mainloop() 