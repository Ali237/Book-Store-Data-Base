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
                INSTER INTO borrowings (member, book_id, start_date, end_date) values (,?,?,date('now'),NULL)''',(email,book_id,))
        # Give the user the borrowing ID
        bid = cursor.lastrowid()
        print(f"you have succesfully borrowed the book, here is the borrowing_id: {bid}")        
    except:
        print("Something wrong happend with INSERT Query")
    




if __name__ == "__main__":
    borrow_book()