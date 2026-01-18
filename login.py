from tkinter import Frame, Label, Entry, Button, messagebox, PhotoImage
from database import connect_database

def login_form(root, on_success):
    frame = Frame(root, bg="#f0f9ff")
    frame.place(relx=0.5, rely=0.5, anchor="center")  # center the frame

    # Optional logo
    try:
        logo = PhotoImage(file="images/librarian_resized.png")
        Label(frame, image=logo, bg="#f0f9ff").pack(pady=(0,10))
        frame.logo = logo  # keep reference to avoid garbage collection
    except:
        pass

    # Title
    Label(frame, text="Library Login", font=("Times New Roman", 24, "bold"),
          bg="#f0f9ff", fg="#010c48").pack(pady=(0,20))

    # Username
    Label(frame, text="Username", font=("Arial", 14), bg="#f0f9ff").pack(anchor="w")
    user_entry = Entry(frame, font=("Arial", 14), bd=2, relief="groove")
    user_entry.pack(pady=5, ipadx=5, ipady=3)

    # Password
    Label(frame, text="Password", font=("Arial", 14), bg="#f0f9ff").pack(anchor="w")
    pass_entry = Entry(frame, font=("Arial", 14), bd=2, relief="groove", show="*")
    pass_entry.pack(pady=5, ipadx=5, ipady=3)

    def attempt_login():
        username = user_entry.get()
        password = pass_entry.get()

        try:
            conn, cursor = connect_database()
             # Query USERS table for matching username/password
            cursor.execute(
                "SELECT role FROM USERS WHERE username=%s AND password=%s",
                (username, password)
            )
            result = cursor.fetchone()

            if result:
                role = result["role"]
                messagebox.showinfo("Login", f"Welcome {username} ({role})")
                frame.destroy()
                on_success(root)
            else:
                messagebox.showerror("Login Failed", "Invalid credentials")

        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")
        finally:
            if conn: 
                conn.close()

    # Login button
    Button(frame, text="Login", font=("Arial", 14, "bold"),
           bg="#048B85", fg="white", cursor="hand2",
           activebackground="#00566b", activeforeground="white",
           width=15, command=attempt_login).pack(pady=20)
    
def logout(root, on_success: callable) -> None:
    # Destroy the main UI
    for widget in root.winfo_children():
        widget.destroy()
    # Show login again
    login_form(root, on_success)
