from tkinter import  *
from tkinter import messagebox, simpledialog
import sqlite3
import getpass
import re
import sys
from datetime import datetime

# Function to connect to the database
def connect_to_database():
    db = simpledialog.askstring("Input", "What is your database?")
    dbpath = "./" + db + ".db" 
    print("Data base path", dbpath)
    conn = sqlite3.connect(dbpath)
    return conn

# Function to create database tables
def create_tables(conn):
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys=ON;')

    c.executescript('''
        CREATE TABLE IF NOT EXISTS members (
            email CHAR(100),
            passwd CHAR(100),
            name CHAR(255) NOT NULL,
            byear INTEGER,
            faculty CHAR(100),
            PRIMARY KEY (email)
        );

        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER,
            title CHAR(255),
            author CHAR(150),
            pyear INTEGER,
            PRIMARY KEY (book_id)
        );

        CREATE TABLE IF NOT EXISTS borrowings(
            bid INTEGER PRIMARY KEY AUTOINCREMENT,
            member CHAR(100) NOT NULL,
            book_id INTEGER NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE,
            FOREIGN KEY (member) REFERENCES members(email),
            FOREIGN KEY (book_id) REFERENCES books(book_id)
        );

        CREATE TABLE IF NOT EXISTS penalties(
            pid INTEGER,
            bid INTEGER NOT NULL,
            amount INTEGER NOT NULL,
            paid_amount INTEGER,
            PRIMARY KEY (pid),
            FOREIGN KEY (bid) REFERENCES borrowings(bid)
        );

        CREATE TABLE IF NOT EXISTS reviews(
            rid INTEGER,
            book_id INTEGER NOT NULL,
            member CHAR(100) NOT NULL,
            rating INTEGER NOT NULL,
            rtext CHAR(255),
            rdate DATE,
            PRIMARY KEY (rid),
            FOREIGN KEY (member) REFERENCES members(email),
            FOREIGN KEY (book_id) REFERENCES books(book_id)
        );
    ''')

    conn.commit()

# Function to handle user login or registration
def is_valid_email(email,conn):
    # Regular expression for a basic email validation
    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    c =conn.cursor()
    # Check if the entered email matches the pattern
    c.execute('''
                SELECT count(*) 
                FROM members
                WHERE email like ?
              ''', (email,))
    does_exests =c.fetchone()[0]
    if re.match(email_pattern, email) and does_exests == 0:
        return True
    else:
        return False

# Get user input for email

# Function to handle user login or registration
def user_authentication(conn):
    c = conn.cursor()
    new_user = False
    while True:
        user_input = simpledialog.askstring("Input", "Are you a user? (y/n)")
        if user_input.lower() == 'y':
            email = simpledialog.askstring("Input", "Email:")
            password = simpledialog.askstring("Input", "Password:", show='*')
            c.execute('SELECT * FROM members WHERE LOWER(email) =LOWER(?) AND passwd = ?', (email, password))
            result = c.fetchone()
            if result:
                messagebox.showinfo("Info", "You are logged in!")
                break
            else:
                messagebox.showerror("Error", "Invalid email or password. Please try again.")
        elif user_input.lower() == 'n':
            messagebox.showinfo("Info", "New User create an account")
            validinput = True
            while validinput:
                email = simpledialog.askstring("Input", "Email:")
                if is_valid_email(email, conn):
                    break
                messagebox.showerror("Error", "Invalid email or email already exists.")
            password = simpledialog.askstring("Input", "Password:", show='*')
            name = simpledialog.askstring("Input", "Name:")
            byear = simpledialog.askinteger("Input", "Enter year:")
            faculty = simpledialog.askstring("Input", "What is your faculty?")
            new_user = True
            try:
                c.execute('''INSERT INTO members VALUES (?, ?, ?, ?, ?);''', (email, password, name, byear, faculty))
                conn.commit()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
            break
        else:
            messagebox.showerror("Error", "Invalid input. Please enter y or n.")
    c.close()
    return email, new_user, conn
# Function to view user profile
def view_profile(email, conn):
    c = conn.cursor()
    # get user info
    c.execute('SELECT * FROM members WHERE email = ?', (email,))
    profile_data = c.fetchone()
    if profile_data:
        print("Name:", profile_data[2])
        print("Email:", profile_data[0])
        print("Birth Year:", profile_data[3])

    ## Fetch and display user's borrowings
        c.execute('SELECT COUNT(*) FROM borrowings WHERE member = ? AND end_date IS NOT NULL', (email,))
        previous_borrowings = c.fetchone()[0]
        print("Previous Borrowings (Returned Books):", previous_borrowings)
        # Currnt borrwoings that are not returned after the deadline 20 days  date (now)
        # gives the current date 

        c.execute('''SELECT COUNT(*) FROM borrowings 
        WHERE member = ?  
                  AND (end_date IS NULL  OR(julianday(date('now')) - julianday(start_date) > 20));''', (email,))   
        current_borrowings = c.fetchone()[0]
        print("Current Borrowings (Unreturned Books):", current_borrowings)

    # Disply over due borrowings
        
    # Penalties information 
        c.execute('''
        SELECT COUNT(pid),SUM(amount - IFNULL(paid_amount,0))
        FROM penalties
        INNER JOIN borrowings USING (bid)
        WHERE amount > IFNULL(paid_amount,0)
        AND member like ? ;''', (email,))

        unpaid_peralties= c.fetchone()
        print(f"Unpaid Penalties: {unpaid_peralties[0]}, Due amont $: {unpaid_peralties[1]} ")



        
  
    else:
        print("User not found.")
    c.close()

# Function to handle returning a book
def returning_book(email, conn):
    c = conn.cursor()
    messagebox.showinfo("Info", "Returning a Book...")

    # Fetch and display user's current borrowings
    c.execute('''
    SELECT bid, book_id, start_date, end_date
    FROM borrowings
    WHERE member = ? AND end_date IS NULL
    ''', (email,))
    current_borrowings = c.fetchall()

    if not current_borrowings:
        messagebox.showinfo("Info", "You have no books to return.")
        return

    msg = "Your current borrowings:\n"
    for row in current_borrowings:
        bid, book_id, start_date, end_date = row
        msg += f"Borrowing ID: {bid}, Book ID: {book_id}, Start Date: {start_date}, End Date: {end_date or 'Not specified'}\n"

    bid_to_return = simpledialog.askinteger("Input", msg + "\nEnter the Borrowing ID of the book you want to return:")
    if bid_to_return not in [row[0] for row in current_borrowings]:
        messagebox.showerror("Error", "Invalid Borrowing ID.")
        return

    returning_date = datetime.now().date()
    days_overdue = (returning_date - current_borrowings[0][2]).days - 20
    penalty = max(0, days_overdue)
    c.execute('''
    UPDATE borrowings
    SET end_date = ?
    WHERE bid = ?;
    ''', (returning_date, bid_to_return))

    if penalty > 0:
        c.execute('''
        INSERT INTO penalties (bid, amount)
        VALUES (?, ?);
        ''', (bid_to_return, penalty))
        messagebox.showinfo("Info", f"Penalty applied: ${penalty}")

    conn.commit()
    messagebox.showinfo("Info", "Book returned successfully.")
    c.close()

# Function to handle user logout
def logout(conn):
    messagebox.showinfo("Info", "Logging out...")
    user_authentication(conn)

# Main function to run the program
def main():
    conn = connect_to_database()
    create_tables(conn)
    email, new_user, conn = user_authentication(conn)

    while True:
        choice = simpledialog.askinteger("Input", "\nPlease Select from the following options:\n1. View profile\n2. Returning a Book\n3. Logout\n4. Exit")
        if choice == 1:
            view_profile(email, conn)
        elif choice == 2:
            returning_book(email, conn)
        elif choice == 3:
            logout(conn)
        elif choice == 4:
            exit()
        else:
            messagebox.showerror("Error", "Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
