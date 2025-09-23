from database import get_connection
import sqlite3

def add_student(id, name, age, phone):
    conn = get_connection()
    cursor = conn.cursor()

    # Check if student ID already exists
    if search_student(id):
        return "exists"

    try:
        cursor.execute(
            "INSERT INTO STUDENTS (id, name, age, phone) VALUES (?, ?, ?, ?)",
            (id, name, age, phone)
        )
        conn.commit()
        return "success"
    except Exception as e:
        return f"error: {e}"
    finally:
        conn.close()


def search_student(student_id):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM STUDENTS WHERE id = ?', (student_id,))
    result = cursor.fetchone()
    conn.close()

    return dict(result) if result else None