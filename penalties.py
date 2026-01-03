from database import connect_database
from tkinter import *
from tkinter import messagebox, ttk
from books import make_optional
from loans import create_loan_treeview
import sqlite3

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
    vertical_scrollbar.pack(side=RIGHT, fill=Y)
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

    return penalty_treeview

def penalties_form(root):
    global backbutton_image

    penalties_frame = Frame(root, bg="white", bd=2, relief=RIDGE)
    penalties_frame.place(x=205, y=98, relheight=1, width=1065)
    header_frame = Frame(penalties_frame, bg="#0B5345", height=40)
    header_frame.pack(fill=X)

    header = Label(header_frame, text="Penalties Management", font=("times new roman", 15, 'bold'), bg="#0B5345", fg="white", anchor=CENTER)
    header.grid(row=0, column=1, sticky="W", padx=350)

    backbutton_image = PhotoImage(file="images\\return.png")
    back_button = Button(header_frame, image=backbutton_image, cursor="hand2", bg="#0B5345",bd=0)
    back_button.grid(row=0, column=0, padx=5)

    # Start of top frame
    top_frame = Frame(penalties_frame, bg="#EEFBF8")
    top_frame.pack(fill=X)

    search_frame1 = Frame(top_frame, bg="#EEFBF8")
    search_frame1.pack()
    search_combobox = ttk.Combobox(search_frame1, values=("Student Id", "Student Name", "Book Title"), font=("times new roman", 12), state="readonly", justify=CENTER)
    search_combobox.set("Search By")
    search_combobox.grid(row=0, column=0, padx=20)
    search_entry = Entry(search_frame1, font=("times new roman", 12), bg="light gray")
    search_entry.grid(row=0, column=1)
    make_optional(search_entry)

    search_button = Button(search_frame1, text="SEARCH", font=("times new roman", 12), bg="#0B5345", fg="white", width=10,
                           cursor="hand2")
    search_button.grid(row=0, column=2, padx=20)

    show_all_button = Button(search_frame1, text="Show All", font=("times new roman", 12), bg="#0B5345", fg="white", width=10,
                             cursor="hand2")
    show_all_button.grid(row=0, column=3)

    loan_treeview = create_loan_treeview(top_frame)
    loan_treeview.pack(pady=(10,0), fill=BOTH, expand=True)
    
    # pentaly_treeview = create_penalty_treeview(top_frame)
    # pentaly_treeview.pack(pady=(10, 0), fill=BOTH, expand=TRUE)

    # Star of bottom frame 
    bot_frame = Frame(penalties_frame, bg="white")
    bot_frame.pack()

    student_id_label = Label(bot_frame, text="Student ID", font=("times new roman", 12), bg="white")
    student_id_label.grid(row=0, column=0)
    student_id_entry = Entry(bot_frame, font=("times new roman", 12), bg="white")
    student_id_entry.grid(row=0, column=1, padx=20, pady=10)

    book_title_label = Label(bot_frame, text="Book Title", font=("times new roman", 12), bg="white")
    book_title_label.grid(row=0, column=2)
    book_title_entry = Entry(bot_frame, font=("times new roman", 12), bg="white")
    book_title_entry.grid(row=0, column=3, padx=20, pady=10)

    loan_id_label = Label(bot_frame, text="Loan ID", font=("times new roman", 12), bg="white")
    loan_id_label.grid(row=1, column=0)
    loan_id_entry = Entry(bot_frame, font=("times new roman", 12), bg="white")
    loan_id_entry.grid(row=1, column=1, padx=20, pady=10)

    amount_label = Label(bot_frame, text="Amount", font=("times new roman", 12), bg="white")
    amount_label.grid(row=1, column=2)
    amount_entry = Entry(bot_frame, font=("times new roman", 12), bg="white")
    amount_entry.grid(row=1, column=3, padx=20, pady=10)

    reason_label = Label(bot_frame, text="Reason", font=("times new roman", 12), bg="white")
    reason_label.grid(row=2, column=0)
    reason_entry = Text(bot_frame, font=("times new roman", 12), bg="white", height=3, width=20)
    reason_entry.grid(row=2, column=1, padx=20, pady=10)

    add_bttn = Button(bot_frame, text="Add", font=("times new roman", 12, "bold"), width=15, fg="white",
                      bg="#0B5345", cursor="hand2")
    add_bttn.grid(row=3, column=0, padx=0, pady=15)

    update_bttn = Button(bot_frame, text="Update", font=("times new roman", 12, "bold"), width=15, fg="white",
                         bg="#0B5345", cursor="hand2")
    update_bttn.grid(row=3, column=1, padx=(20,0), pady=15)

    delete_bttn = Button(bot_frame, text="Delete", font=("times new roman", 12, "bold"), width=15, fg="white",
                      bg="#0B5345", cursor="hand2")
    delete_bttn.grid(row=3, column=2, padx=(20,0), pady=15)

    clear_bttn = Button(bot_frame, text="Clear", font=("times new roman", 12, "bold"), width=15, fg="white",
                      bg="#0B5345", cursor="hand2")
    clear_bttn.grid(row=3, column=3, padx=(20,0), pady=15)

    show_penalties_bttn = Button(bot_frame, text="View Penalties", font=("times new roman", 12, "bold"), width=15, fg="white",
                      bg="#0B5345", cursor="hand2")
    show_penalties_bttn.grid(row=4, column=1, columnspan=2, padx=(20,0))