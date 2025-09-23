from database import get_connection
from loans import search_loan

def add_penalty(student_id, book_name, loan_date, reason):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Check if loan record exists
        loan = search_loan(student_id, book_name, loan_date)
        if loan is None:
            return "No loan record found for this student and book."
        
        # Insert penalty record
        loan_id = loan['id']
        cursor.execute("INSERT INTO PENALTIES (student_id, book_name, loan_id, reason) VALUES (?, ?, ?, ?)",
                    (student_id, book_name, loan_id, reason))
            
        # Update student's total penalty
        cursor.execute("UPDATE STUDENTS SET total_penalty = total_penalty + 1 WHERE id = ?", (student_id,))
        conn.commit()
        return "Penalty added successfully."
    except Exception as e:
        return f"error: {str(e)}"   
    finally:
        conn.close()

       
        
