import sqlite3
import getpass
import re
from datetime import datetime
from datetime import date
import uuid
#from types import NoneType


# Function to connect to the database
def connect_to_database():
    # lets get started
    # take the input for data base
    db = input('What is your database?')
    dbpath = "./" + db + ".db" 
    print("Data base path",dbpath)
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
    
#     # data input 
#     # Insert data into the members table
#     c.executemany("INSERT OR IGNORE INTO members VALUES (?, ?, ?, ?, ?);", [
#         ('user1@email.com', 'password1', 'User One', 1990, 'Science'),
#         ('user2@email.com', 'password2', 'User Two', 1985, 'Arts'),
#         ('user3@email.com', 'password3', 'User Three', 1992, 'Engineering'),
#         ('user4@email.com', 'password4', 'User Four', 1988, 'Business'),
#         ('user5@email.com', 'password5', 'User Five', 1995, 'Medicine'),
#         # Add more members as needed
#     ])

#     # Insert data into the books table
#     c.executemany("INSERT OR IGNORE INTO books VALUES (?, ?, ?, ?);", [
#         (1, 'The Great Gatsby', 'F. Scott Fitzgerald', 1925),
#         (2, 'To Kill a Mockingbird', 'Harper Lee', 1960),
#         (3, '1984', 'George Orwell', 1949),
#         (4, 'Pride and Prejudice', 'Jane Austen', 1813),
#         (5, 'The Catcher in the Rye', 'J.D. Salinger', 1951),
#         (6, 'desert Incounters', 'Kunod Helmboy', 1920),
#         # Add more books as needed
#     ])

#     # Insert data into the borrowings table
#     c.executemany("INSERT OR IGNORE INTO borrowings VALUES (?, ?, ?, ?, ?);", [
#         (1, 'user1@email.com', 1, '2024-03-10', '2024-03-20'),
#         (2, 'user2@email.com', 2, '2024-03-05', '2024-03-15'),
#         (3, 'user3@email.com', 3, '2024-03-12', 'NULL'),
#         (4, 'user4@email.com', 4, '2024-03-08', '2024-03-18'),
#         (5, 'user5@email.com', 5, '2024-03-15', '2024-03-25'),
#         (6, 'user2@email.com', 6, '2024-02-01', 'NULL'),
#         # Add more borrowings as needed
#     ])
#     c.execute('''update borrowings set end_date =NULL where bid =2;

#             ''')

#     # Insert data into the penalties table
#     c.executemany("INSERT OR IGNORE INTO penalties VALUES (?, ?, ?, ?);", [
#         (1, 1, 5, None),
#         (2, 2, 8, 4),
#         (3, 3, 3, None),
#         (4, 4, 10, 7),
#         (5, 5, 6, None),
#         # Add more penalties as needed
#     ])

#     # Insert data into the reviews table
#     c.executemany("INSERT OR IGNORE INTO reviews VALUES (?, ?, ?, ?, ?, ?);", [
#         (1, 1, 'user1@email.com', 4, 'Enjoyed the book!', '2024-03-12'),
#         (2, 2, 'user2@email.com', 5, 'A classic!', '2024-03-08'),
#         (3, 3, 'user3@email.com', 3, 'Not bad.', '2024-03-15'),
#         (4, 4, 'user4@email.com', 5, 'Highly recommended!', '2024-03-18'),
#         (5, 5, 'user5@email.com', 4, 'Interesting read.', '2024-03-20'),
#         # Add more reviews as needed
#     ])

# # Commit changes to the database
#     conn.commit()

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
        user_input = input("Are you a user? \n Please answer with y or n: ").lower()
        if user_input == 'y':
            email = input("email: ").lower()   # what if the emails saved in upper case
            password = getpass.getpass("Password: ")
            c.execute('SELECT * FROM members WHERE LOWER(email) =LOWER(?) AND passwd = ?', (email, password)) # both eamils are converted to lower case befre being compared
            result = c.fetchone()
            if result:
                print("You are logged in!")
                break
            else:
                print("Invalid email or password. Please try again.")
        elif user_input == 'n':
            print("New User create an account")
            validinput = True
            while validinput:
                email = input("email: ").lower()

                if is_valid_email(email,conn):
                    break
                print("Invalid eamil please enter again or email already exixts\n") 
               # We have an issue a new user is not saved in the data base and in the members table # 
            password = getpass.getpass("Input a Password: ")
            name = input("Name: ")
            byear = input("Enter year: ")
            faculty = input("What is your faculty? ")
            new_user = True
            try:
                c.execute('''INSERT INTO members VALUES (:email, :psd, :name, :year, :fact);
                        ''',{"email":email,"psd":password, "name":name,"year":byear,"fact":faculty})
                conn.commit()
            except Exception as e:
                print("An error occurred: ",e)
            break
        else:
            print("Invalid input. Please enter y or n.")
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
#     
    c = conn.cursor()
    print("Returning a Book...")

    # Fetch and display user's current borrowings
    c.execute('''
    SELECT bid, book_id, start_date, end_date
    FROM borrowings
    WHERE member = ? AND end_date IS NULL
    ''', (email,))
    current_borrowings = c.fetchall()

    if not current_borrowings:
        print("You have no books to return.")
        return

    print("Your current borrowings:")
    for row in current_borrowings:
        bid, book_id, start_date, end_date = row
        print(f"Borrowing ID: {bid}, Book ID: {book_id}, Start Date: {start_date}, End Date: {end_date or 'Not specified'}")

    # Choose a borrowing to return
    while True:
        try:
            bid_to_return = int(input("Enter the Borrowing ID of the book you want to return: "))
            if bid_to_return in [row[0] for row in current_borrowings]:
                break
            else:
                print("Invalid Borrowing ID. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Record today's date as the returning date
    returning_date = datetime.now().date()

    # Calculate penalties
    c.execute('''
    SELECT julianday(?) - julianday(start_date) - 20
    FROM borrowings
    WHERE bid = ?;
    ''', (returning_date, bid_to_return))
    days_overdue = c.fetchone()[0]
    penalty = max(0, days_overdue)  # Penalty is $1 per day after the deadline

    # Update the borrowings table with the returning date
    c.execute('''
    UPDATE borrowings
    SET end_date = ?
    WHERE bid = ?;
    ''', (returning_date, bid_to_return))

    # Apply penalty if applicable
    if penalty > 0:
        c.execute('''
        INSERT INTO penalties (bid, amount)
        VALUES (?, ?);
        ''', (bid_to_return, penalty))
        print(f"Penalty applied: ${penalty}")

    # Ask user for a review
    review_choice = input("Do you want to write a review for this book? (y/n): ").lower()
    if review_choice == 'y':
        while True:
            rating = int(input("Enter a rating for the book (1-5): ")) # limit the input between 1-5
            if  1 <= rating <= 5:
                break
            else:
                print("Invalid rating. Please enter a number between 1 and 5.")
        review_text = input("Enter your review: ")
        review_date = datetime.now().date()

        # Insert review into the reviews table
        c.execute('''
        INSERT INTO reviews (book_id, member, rating, rtext, rdate)
        VALUES (?, ?, ?, ?, ?);
        ''', (book_id, email, rating, review_text, review_date))
        print("Review added successfully.")

    conn.commit()
    print("Book returned successfully.")
    c.close()

#----------------------------------------------------------------------------------------------------------#
# Function to handle searching for books
def search_books(conn,cursor,email):
    keyword = input("Plesase enter a keyword to find a book:")
    print("Searching for Books...")
    keyword = f'%{keyword}%'  # Prepare the keyword for a LIKE query
    e =email
    # Getting Books that are not borrowed/available
    available_books_query = '''WITH tmptb AS (
                               SELECT book_id, AVG(rating) AS avg_rating
                               FROM reviews
                               GROUP BY book_id)
                               SELECT b.book_id, b.title, b.author, b.pyear, IFNULL(tb.avg_rating, 0) AS avg_rating, 'Available' AS status
                               FROM books b
                               LEFT JOIN tmptb tb ON b.book_id = tb.book_id
                               WHERE (b.title LIKE ? OR b.author LIKE ?) AND b.book_id NOT IN (SELECT book_id FROM borrowings Where end_date IS NULL);'''
    cursor.execute(available_books_query, (keyword, keyword))
    available_books = cursor.fetchall()
    
    # Query for unavailable books
    unavailable_books_query = '''WITH tmptb AS (
                                  SELECT book_id, AVG(rating) AS avg_rating
                                  FROM reviews
                                  GROUP BY book_id)
                                 SELECT DISTINCT b.book_id, b.title, b.author, b.pyear, IFNULL(tb.avg_rating, 'No Rating') AS avg_rating, 'Not Available' AS status
                                 FROM borrowings
                                 INNER JOIN books b USING (book_id)
                                 LEFT JOIN tmptb tb ON b.book_id = tb.book_id
                                 WHERE (b.title LIKE ? OR b.author LIKE ?) AND end_date IS NULL ;'''
    cursor.execute(unavailable_books_query, (keyword, keyword))
    unavailable_books = cursor.fetchall()
    
    # uninion both tuples to get all books
    all_books = available_books + unavailable_books 
    
    # check if anybooks match with keyword given
    if not all_books:
        print("No books found.")
        return
    
    for i, book in enumerate(all_books, 1):
        print(f"{i}. ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Year: {book[3]}, Avg. Rating: {book[4]}, Status: {book[5]}")

    # Ask user to select a book to borrow
    selection = input("Enter the number of the book you would like to borrow (or 'exit' to cancel): ")
    if selection.lower() == 'exit':
        return
   
    borrow_book(int(selection),e,cursor)  # Pass book id if available
    conn.commit()
      
#-----------------------------------------------------------------------#
# Function to handle borrowing a book
def borrow_book(book_id,email,cursor):
    # Written By Moath Ghanem on Marhc,14th,2024
    # search and check that book_id is availabe and a valid book_id
    try:
        cursor.execute('''
                SELECT book_id
                   FROM books b
                   WHERE book_id = ?
                   AND book_id NOT IN (
                   SELECT book_id
                   FROM books b
                   JOIN borrowings br USING (book_id)
                   WHERE br.end_date IS NULL
                   );''',(book_id,))
    except:
        print("Connection error OR querry has syntax error")

    row_flag = cursor.fetchone()
    if(isinstance(row_flag,NoneType)):
        print("The book_id you entered is not available")
        return
    
    # raching this means that book_id is valid and available. So update the book_id status
    try:
        cursor.execute('''
                INSERT INTO borrowings (member, book_id, start_date, end_date) values (?,?,date('now'),NULL)''',(email,book_id,))
        
       
              
    except:
        print("Something wrong happend with INSERT Query")
        
    
    # Give the user the borrowing ID
    bid = cursor.lastrowid
    print(f"you have succesfully borrowed the book, here is the borrowing_id: {bid}") 

#-------------------------------------------------------------#
#-------------------------------------------------------------#
# Function to handle paying a penalty
def pay_penalty(conn,email):
    print("Paying a Penalty...")
    cursor = conn.cursor()
    cursor.execute('''SELECT pid, amount, IFNULL(paid_amount,0)
                   FROM penalties
                   INNER JOIN borrowings USING (bid)
                   WHERE amount > IFNULL(paid_amount,0)
                   AND member LIKE ?
                   ''',(email,))
    penalties = cursor.fetchall()
    if not penalties:
        print("You have no penalties")
        return
    for penalty in penalties:
        print(f"PID: {penalty[0]}, Amount: {penalty[1]}, Paid Amount: {penalty[2]}")
    pid = input("Write the pid of the penalty you want to pay: ")
    try:
        cursor.execute('''
            SELECT amount, paid_amount
            FROM penalties
            INNER JOIN borrowings USING (bid)
            WHERE member like ?
            AND pid = ?;''',(email,pid))
    
    except:
        print("Wrong PID")
        return
    
    pid_info = cursor.fetchone()
    if isinstance(pid_info, NoneType):
        print("Wrong PID")
        return
    amount = pid_info[0]
    amount_paid = pid_info[0]
    
    amount_to_pay = amount - amount_paid
    paying = input("Enter Amount you're willing to pay: ")
    remaining = amount_to_pay - int(paying)

    if(remaining <= 0):
        # paid full
        remaining = abs(remaining)
    try:
            cursor.execute('''
                UPDATE penalties
                SET paid_amount = IFNULL(paid_amount,0) + ?
                WHERE pid IN (
                        SELECT p.pid
                        FROM penalties p
                        JOIN borrowings b ON p.bid = b.bid
                        WHERE b.member LIKE ? AND p.pid = ?
                    );''', (paying, email, pid))
            conn.commit()  # Commit changes if necessary
    except:
        print("error in paying penalty") 

# Function to handle user logout
def logout(conn):
    print("Logging out...")
    #exit()
    # prompt the user to login again 
    user_authentication(conn)
# Main function to run the program
def main():
    conn = connect_to_database()
    create_tables(conn)
    email, new_user, conn = user_authentication(conn)

    while True:
        print("\n Please Select from the following options: ")
        print("1. View profile")
        print("2. Returning a Book")
        print("3. Search for Books")
        print("4. Pay a Penalty")
        print("5. Logout")
        print("6. Exit")
        choice = input("Enter the number of your choice: ")

        if choice == '1':
            view_profile(email, conn)
        elif choice == '2':
            returning_book(email, conn)
        elif choice == '3':
            search_books(conn,conn.cursor(),email)
        elif choice == '4':
            pay_penalty(conn,email)
        elif choice == '5':
            email, new_user, conn = user_authentication(conn)
        elif choice == '6':
           exit()
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
