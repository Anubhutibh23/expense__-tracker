import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import mysql.connector as mysql

current_user = None

# Define the color scheme
PRIMARY_COLOR = "#3498db"
SECONDARY_COLOR = "#2ecc71"
BACKGROUND_COLOR = "#ecf0f1"
TEXT_COLOR = "#2c3e50"
WHITE_COLOR = "#ffffff"

def login_window():
    global current_user
    login_window = tk.Tk()
    login_window.title("Expense Tracker - Login")
    login_window.geometry("400x300")
    login_window.configure(bg=BACKGROUND_COLOR)

    def validate_login():
        global current_user
        username = username_entry.get()
        password = password_entry.get()

        if not (username and password):
            messagebox.showwarning("Login Error", "Please enter username and password.")
            return

        conn = mysql.connect(host="localhost", user="root", password="anu@123", database="expense_tracker")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            current_user = username
            login_window.destroy()
            main_application()
        else:
            messagebox.showerror("Login Error", "Invalid username or password.")

        conn.close()

    def open_registration_window():
        login_window.destroy()
        registration_window()

    tk.Label(login_window, text="Username:", font=("Arial", 14), bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=10)
    username_entry = tk.Entry(login_window, font=("Arial", 12))
    username_entry.pack(pady=5)

    tk.Label(login_window, text="Password:", font=("Arial", 14), bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=10)
    password_entry = tk.Entry(login_window, show='*', font=("Arial", 12))
    password_entry.pack(pady=5)

    login_button = tk.Button(login_window, text="Login", font=("Arial", 14), bg=PRIMARY_COLOR, fg=WHITE_COLOR, command=validate_login)
    login_button.pack(pady=20)

    register_button = tk.Button(login_window, text="Register", font=("Arial", 14), bg=SECONDARY_COLOR, fg=WHITE_COLOR, command=open_registration_window)
    register_button.pack(pady=10)

    login_window.mainloop()

def registration_window():
    registration_window = tk.Tk()
    registration_window.title("Expense Tracker - Registration")
    registration_window.geometry("500x400")
    registration_window.configure(bg=BACKGROUND_COLOR)

    def register_user():
        username = username_entry.get()
        password = password_entry.get()
        email = email_entry.get()

        if not (username and password and email):
            messagebox.showwarning("Registration Error", "Please enter all fields.")
            return

        conn = mysql.connect(host="localhost", user="root", password="anu@123", database="expense_tracker")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, password, email))
        conn.commit()
        messagebox.showinfo("Registration Success", "User registered successfully.")
        registration_window.destroy()
        login_window()
        conn.close()

    tk.Label(registration_window, text="Username:", font=("Arial", 14), bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=10)
    username_entry = tk.Entry(registration_window, font=("Arial", 12))
    username_entry.pack(pady=5)

    tk.Label(registration_window, text="Password:", font=("Arial", 14), bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=10)
    password_entry = tk.Entry(registration_window, show='*', font=("Arial", 12))
    password_entry.pack(pady=5)

    tk.Label(registration_window, text="Email:", font=("Arial", 14), bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=10)
    email_entry = tk.Entry(registration_window, font=("Arial", 12))
    email_entry.pack(pady=5)

    register_button = tk.Button(registration_window, text="Register", font=("Arial", 14), bg=PRIMARY_COLOR, fg=WHITE_COLOR, command=register_user)
    register_button.pack(pady=20)
    back_to_login_button = tk.Button(registration_window, text="Back to Login", bg="#ff4d4d", fg=TEXT_COLOR, font=("Arial", 14), command=lambda: [registration_window.destroy(), login_window()])
    back_to_login_button.pack(pady=10)
    registration_window.mainloop()

def main_application():
    global main_window
    main_window = tk.Tk()
    main_window.title("Expense Tracker - Main Application")
    main_window.geometry("1250x800")
    main_window.configure(bg=BACKGROUND_COLOR)

    button_frame = tk.Frame(main_window, bg=BACKGROUND_COLOR)
    button_frame.pack(side=tk.LEFT, fill=tk.Y)

    button_font = Font(family="Arial", size=14, weight="bold")

    dashboard_button = tk.Button(button_frame, text="Dashboard", command=lambda: notebook.select(dashboard_frame), height=8, width=25, font=button_font, bg=PRIMARY_COLOR, fg=WHITE_COLOR)
    dashboard_button.pack(fill=tk.X, pady=10)

    add_expense_button = tk.Button(button_frame, text="Add Expense", command=lambda: notebook.select(add_edit_frame), height=8, width=25, font=button_font, bg=PRIMARY_COLOR, fg=WHITE_COLOR)
    add_expense_button.pack(fill=tk.X, pady=5)

    add_income_button = tk.Button(button_frame, text="Add/Edit Income", command=lambda: notebook.select(add_edit_income_frame), height=8, width=25, font=button_font, bg=PRIMARY_COLOR, fg=WHITE_COLOR)
    add_income_button.pack(fill=tk.X, pady=5)

    all_expenses_button = tk.Button(button_frame, text="All Expenses", command=lambda: notebook.select(all_expenses_frame), height=8, width=25, font=button_font, bg=PRIMARY_COLOR, fg=WHITE_COLOR)
    all_expenses_button.pack(fill=tk.X, pady=5)

    notebook_frame = tk.Frame(main_window, bg=BACKGROUND_COLOR)
    notebook_frame.pack(side=tk.RIGHT, expand=True, fill='both')

    notebook = ttk.Notebook(notebook_frame)
    notebook.pack(expand=True, fill='both')

    dashboard_frame = tk.Frame(notebook, bg=BACKGROUND_COLOR )
    notebook.add(dashboard_frame, text="")
    display_dashboard(dashboard_frame)

    add_edit_frame = tk.Frame(notebook, bg=BACKGROUND_COLOR )
    notebook.add(add_edit_frame, text="")
    display_add_edit_expense(add_edit_frame)

    add_edit_income_frame = tk.Frame(notebook, bg=BACKGROUND_COLOR )
    notebook.add(add_edit_income_frame, text="")
    display_add_edit_income(add_edit_income_frame)

    all_expenses_frame = tk.Frame(notebook, bg=BACKGROUND_COLOR )
    notebook.add(all_expenses_frame, text="")
    display_all_expenses(all_expenses_frame)
    logout_button = tk.Button(button_frame, text="Logout", command=logout, height=2, width=20, font=button_font, bg="#ff4d4d", fg=TEXT_COLOR)
    logout_button.pack(fill=tk.X, pady=10)
    logout_button.bind("<Enter>", lambda e: logout_button.config(bg="#cc0000"))
    logout_button.bind("<Leave>", lambda e: logout_button.config(bg="#ff4d4d"))
    main_window.mainloop()
    
def logout():
    global main_window, current_user
    if messagebox.askyesno("Logout", "Are you sure you want to log out?"):
        main_window.destroy()
        current_user = None
        login_window()
def display_dashboard(frame):
    tk.Label(frame, text="Welcome to Dashboard", bg=BACKGROUND_COLOR , fg=PRIMARY_COLOR, font=("Arial", 28)).pack(pady=20)

    tk.Label(frame, text="Total Expenses:", bg=WHITE_COLOR, fg=TEXT_COLOR, font=("Arial", 18), anchor='center').pack(fill=tk.X, pady=5)
    total_expenses_label = tk.Label(frame, text="", bg=WHITE_COLOR, fg=TEXT_COLOR, font=("Arial", 18), anchor='center')
    total_expenses_label.pack(fill=tk.X, pady=5)

    tk.Label(frame, text="Total Income:", bg=WHITE_COLOR, fg=TEXT_COLOR, font=("Arial", 18), anchor='center').pack(fill=tk.X, pady=5)
    total_income_label = tk.Label(frame, text="", bg=WHITE_COLOR, fg=TEXT_COLOR, font=("Arial", 18), anchor='center')
    total_income_label.pack(fill=tk.X, pady=5)

    tk.Label(frame, text="Balance:", bg=WHITE_COLOR, fg=TEXT_COLOR, font=("Arial", 18), anchor='center').pack(fill=tk.X, pady=5)
    balance_label = tk.Label(frame, text="", bg=WHITE_COLOR, fg=TEXT_COLOR, font=("Arial", 18), anchor='center')
    balance_label.pack(fill=tk.X, pady=5)

    def update_dashboard():
        conn = mysql.connect(host="localhost", user="root", password="anu@123", database="expense_tracker")
        cursor = conn.cursor()

        cursor.execute("SELECT SUM(amount) FROM expenses WHERE user_id = (SELECT id FROM users WHERE username = %s)", (current_user,))
        total_expenses = cursor.fetchone()[0] or 0
        total_expenses_label.config(text=f"₹ {total_expenses:.2f}")

        cursor.execute("SELECT SUM(amount) FROM income WHERE user_id = (SELECT id FROM users WHERE username = %s)", (current_user,))
        total_income = cursor.fetchone()[0] or 0
        total_income_label.config(text=f"₹ {total_income:.2f}")

        balance = total_income - total_expenses
        balance_label.config(text=f"₹ {balance:.2f}")

        conn.close()

        
    update_button = tk.Button(frame,bg=PRIMARY_COLOR, fg=WHITE_COLOR, text="Update Dashboard", font=("Arial", 14), command=update_dashboard)
    update_button.pack(pady=30)


    update_dashboard()

def display_add_edit_expense(frame):
    tk.Label(frame, text="Add/Edit Expense", bg=BACKGROUND_COLOR , fg=PRIMARY_COLOR, font=("Arial", 28)).pack(pady=20)

    tk.Label(frame, text="Date (DD-MM-YYYY):", bg=WHITE_COLOR, fg=TEXT_COLOR, font=("Arial", 14)).pack()
    date_entry = DateEntry(frame, date_pattern="dd-mm-yyyy", font=("Arial", 12))
    date_entry.pack(pady=5)

    tk.Label(frame, text="Category:", bg=WHITE_COLOR, fg=TEXT_COLOR, font=("Arial", 14)).pack()
    category_entry = tk.Entry(frame, font=("Arial", 12))
    category_entry.pack(pady=5)

    tk.Label(frame, text="Amount:", bg=WHITE_COLOR, fg=TEXT_COLOR, font=("Arial", 14)).pack()
    amount_entry = tk.Entry(frame, font=("Arial", 12))
    amount_entry.pack(pady=5)

    tk.Label(frame, text="Description:", bg=WHITE_COLOR, fg=TEXT_COLOR, font=("Arial", 14)).pack()
    description_entry = tk.Text(frame, height=5, font=("Arial", 12))
    description_entry.pack(pady=5)

    def add_edit_expense():
        date = date_entry.get_date()
        category = category_entry.get()
        amount = amount_entry.get()
        description = description_entry.get("1.0", tk.END).strip()

        if not (date and category and amount):
            messagebox.showwarning("Add Expense", "Please enter all required fields.")
            return

        conn = mysql.connect(host="localhost", user="root", password="anu@123", database="expense_tracker")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO expenses (user_id, expanse_date, category, amount, description) VALUES ((SELECT id FROM users WHERE username = %s), %s, %s, %s, %s)",
                       (current_user, date, category, amount, description))
        conn.commit()
        messagebox.showinfo("Add/Edit Expense", "Expense added successfully.")
        conn.close()

        date_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        description_entry.delete("1.0", tk.END)

    add_edit_button = tk.Button(frame, text="Add/Edit Expense", font=("Arial", 14), bg=PRIMARY_COLOR, fg=WHITE_COLOR, command=add_edit_expense)
    add_edit_button.pack(pady=10)


def display_add_edit_income(frame):
    tk.Label(frame, text="Add/Edit Income", bg=BACKGROUND_COLOR , fg=PRIMARY_COLOR, font=("Arial", 28)).pack(pady=20)

    tk.Label(frame, text="Date (DD-MM-YYYY):", bg=WHITE_COLOR, fg=TEXT_COLOR, font=("Arial", 14)).pack()
    income_date_entry = DateEntry(frame, date_pattern="dd-mm-yyyy", font=("Arial", 12))
    income_date_entry.pack(pady=5)

    tk.Label(frame, text="Amount:", bg=WHITE_COLOR, fg=TEXT_COLOR, font=("Arial", 14)).pack()
    income_amount_entry = tk.Entry(frame, font=("Arial", 12))
    income_amount_entry.pack(pady=5)

    tk.Label(frame, text="Description:", bg=WHITE_COLOR, fg=TEXT_COLOR, font=("Arial", 14)).pack()
    income_description_entry = tk.Text(frame, height=5, font=("Arial", 12))
    income_description_entry.pack(pady=5)

    def add_edit_income():
        income_date = income_date_entry.get_date()
        income_amount = income_amount_entry.get()
        income_description = income_description_entry.get("1.0", tk.END).strip()

        if not (income_date and income_amount):
            messagebox.showwarning("Add Income", "Please enter all required fields.")
            return

        conn = mysql.connect(host="localhost", user="root", password="anu@123", database="expense_tracker")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO income (user_id, income_date, amount, description) VALUES ((SELECT id FROM users WHERE username = %s), %s, %s, %s)",
                       (current_user, income_date, income_amount, income_description))
        conn.commit()
        messagebox.showinfo("Add Income", "Income added successfully.")
        conn.close()

        income_date_entry.delete(0, tk.END)
        income_amount_entry.delete(0, tk.END)
        income_description_entry.delete("1.0", tk.END)

    add_edit_income_button = tk.Button(frame, text="Add/Edit Income", font=("Arial", 14), bg=PRIMARY_COLOR, fg=WHITE_COLOR, command=add_edit_income)
    add_edit_income_button.pack(pady=10)


def display_all_expenses(frame):
    tk.Label(frame, text="All Expenses", bg=BACKGROUND_COLOR , fg=PRIMARY_COLOR, font=("Arial", 28)).pack(pady=20)

    all_expenses_text = tk.Text(frame, height=35, width=125, font=("Arial", 12), bg=WHITE_COLOR, fg=TEXT_COLOR)
    all_expenses_text.pack(pady=10)

    def fetch_all_expenses():
        conn = mysql.connect(host="localhost", user="root", password="anu@123", database="expense_tracker")
        cursor = conn.cursor()
        cursor.execute("SELECT expanse_date, category, amount, description FROM expenses WHERE user_id = (SELECT id FROM users WHERE username = %s)", (current_user,))
        results = cursor.fetchall()

        all_expenses_text.delete("1.0", tk.END)
        if results:
            for result in results:
                expanse_date, category, amount, description = result
                expanse_date = expanse_date.strftime('%d-%m-%Y')
                all_expenses_text.insert(tk.END, f"Date: {expanse_date}, Category: {category}, Amount: ₹{amount:.2f}, Description: {description}\n\n")
        else:
            all_expenses_text.insert(tk.END, "No expenses found.")

        conn.close()

    fetch_all_expenses()

    refresh_button = tk.Button(frame, text="Refresh", font=("Arial", 18), bg=PRIMARY_COLOR, fg=WHITE_COLOR, command=fetch_all_expenses)
    refresh_button.pack(pady=10)

    def auto_refresh():
        fetch_all_expenses()
        frame.after(5000, auto_refresh)

    auto_refresh()

login_window()
