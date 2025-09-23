import sqlite3

def get_connection():
    return sqlite3.connect("library.db")

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Create STUDENTS table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS STUDENTS (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            phone TEXT NOT NULL,
            total_penalty INT DEFAULT 0
        );
    """)

    # Create BOOKS table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS BOOKS (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            quantity INTEGER NOT NULL
        );
    """)

    # Create LOANS table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS LOANS (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            book_name TEXT NOT NULL,
            loan_date TEXT NOT NULL,
            return_date TEXT,
            status TEXT,
            FOREIGN KEY (student_id) REFERENCES STUDENTS(id)
        );
    """)

    # Create PENALTIES table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS PENALTIES (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            loan_id INTEGER NOT NULL,
            book_name TEXT NOT NULL,
            reason TEXT,
            FOREIGN KEY (student_id) REFERENCES STUDENTS(id),
            FOREIGN KEY (loan_id) REFERENCES LOANS(id)
        );
    """)

    conn.commit()
    conn.close()
