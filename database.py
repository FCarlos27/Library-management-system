from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import pymysql

def connect_database():
    try: 
        connection = pymysql.connect(host="localhost", user="root", password="", database="library_system")
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        return connection, cursor
    except:
        messagebox.showerror("Error", "Couldn't connect to database, please try agayn", )
        return None, None
    

def initialize_database():
    conn, cursor = connect_database()

    cursor.execute("CREATE DATABASE IF NOT EXISTS library_system")
    cursor.execute("USE library_system")

    # Create STUDENTS table
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS STUDENTS (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(100) NOT NULL,
                birthdate DATE,
                phone VARCHAR(20) NOT NULL,
                email VARCHAR(100),
                address VARCHAR(255),
                total_penalty INT DEFAULT 0
            ) ENGINE=InnoDB;
    """)

    # Create BOOKS table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS BOOKS (
            id INT PRIMARY KEY AUTO_INCREMENT,
            title VARCHAR(255) NOT NULL,
            author VARCHAR(255) NOT NULL,
            quantity INT NOT NULL,
            year INT NOT NULL,
            edition VARCHAR(50),
            language VARCHAR(15)
        ) ENGINE=InnoDB;
    """)

    # Create LOANS table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS LOANS (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    book_id INT NOT NULL,
    loan_date DATE NOT NULL,
    return_date DATE,
    status VARCHAR(50),
    FOREIGN KEY (student_id) REFERENCES STUDENTS(id),
    FOREIGN KEY (book_id) REFERENCES BOOKS(id)
    ) ENGINE=InnoDB;
    """)

    # Create PENALTIES table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS PENALTIES (
            id INT PRIMARY KEY AUTO_INCREMENT,
            student_id INT NOT NULL,
            loan_id INT NOT NULL,
            book_name VARCHAR(255) NOT NULL,
            reason TEXT,
            FOREIGN KEY (student_id) REFERENCES STUDENTS(id),
            FOREIGN KEY (loan_id) REFERENCES LOANS(id)
        ) ENGINE=InnoDB;
    """)

    conn.commit()
    conn.close()

initialize_database()