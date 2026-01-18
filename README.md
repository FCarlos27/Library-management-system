# Library Management System

A desktop application built with Python Tkinter and MySQL. It provides a login system, a styled dashboard, and modules to manage books, students, loans, and penalties. The project demonstrates CRUD operations, secure login with parameterized queries, and a user-friendly interface with custom icons and flashcards.

## Features
- Login form with database-backed authentication
- Tkinter UI with custom images and icons
- Flashcards showing totals (books, students, loans)
- Menu navigation for Books, Students, Loans, Penalties, and Exit
- MySQL integration with a `USERS` table for credential storage

## Requirements
- Python 3.x
- Tkinter (comes with Python)
- PyMySQL
- MySQL server

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/username/library-management-system.git
2. Install dependencies:
   pip install pymysql
3. Create a MySQL database named library_system.
4. Run the initialization script in database.py to create the USERS table.
5. Insert at least one user into the USERS table for login.
6. Run the application:
   py app.py
7. Sign in to open the dashboard where you can manage books, students, loans, and penalties


