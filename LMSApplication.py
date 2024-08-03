import tkinter.ttk as tkrtk
import tkinter as tk
import datetime
import sqlite3

import os

def switch_to_tab(tab_index):
    notebook.select(tab_index)

def display_book_copies():
    with sqlite3.connect('proj2part3/LMS.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM BOOK_COPIES")
        book_copies = cur.fetchall()
        
        # Clear the existing content in the treeview
        for row in book_copies_tree.get_children():
            book_copies_tree.delete(row)
        
        # Insert the fetched rows into the treeview
        for row in book_copies:
            book_copies_tree.insert("", "end", values=row)

def submit1():
    print("user checked out " + enter_textbox.get() + "\n")

    submit_conn = sqlite3.connect('proj2part3/LMS.db')
    submit_cur = submit_conn.cursor()

    # getting Book id from input title
    submit_cur.execute("SELECT Book_id FROM BOOK WHERE Title = ?", (enter_textbox.get(),))
    test_output = submit_cur.fetchall()
    book_id = test_output[0][0]

    # print("book id: " + str(book_id))

    date_out = datetime.date.today()
    due_date = date_out + datetime.timedelta(days=30)

    submit_cur.execute("UPDATE BOOK_COPIES SET No_Of_Copies = No_Of_Copies - 1\
                       WHERE Book_Id = ? AND Branch_Id = ?", (book_id, branch_textbox.get()))

    submit_cur.execute("INSERT INTO BOOK_LOANS(Book_Id, Branch_Id, Card_No, Date_out, Due_date) \
                       VALUES(?, ?, ?, ?, ?)", (book_id, branch_textbox.get(), card_no_textbox.get(), date_out, due_date))
    submit_conn.commit()

    submit_cur.execute("SELECT Name FROM BORROWER WHERE Card_No = ?", (card_no_textbox.get(),))
    test_output = submit_cur.fetchall()
    borrower_name = test_output[0][0]

    # print("borrower name " + borrower_name)

    display_book_copies()
    message_label.config(text=borrower_name + " succesfully checked out " + enter_textbox.get() + "!", font = ("aerial", 12, "bold"))
    enter_textbox.delete(0,tk.END)
    branch_textbox.delete(0, tk.END)
    card_no_textbox.delete(0, tk.END)
#req2
def submit2():
    submit_conn = sqlite3.connect('proj2part3/LMS.db')
    
    submit_cur = submit_conn.cursor()
    submit_cur.execute("INSERT INTO BORROWER (Name, Address, Phone) VALUES (:Name, :Address, :Phone)",
        {
            'Name': Name.get(),
            'Address': Address.get(),
            'Phone': Phone.get()
        })
    submit_conn.commit()
    submit_conn.close()
def input_query():

    iq = sqlite3.connect('proj2part3/LMS.db')
    
    iq_cur = iq.cursor()
    iq_cur.execute("Select Card_No FROM BORROWER WHERE Name = ? AND Address = ? AND Phone = ?",
                   (Name.get(), Address.get(), Phone.get()))
    
    records = iq_cur.fetchall()

    iq_label = tk.Label(tab2, text = records)
    iq_label.grid(row = 9, column = 0, columnspan = 2)

    iq.commit()
    iq.close()

#req 4
# search value
def search(listbox):
    
    selection = listbox.get(listbox.curselection())

    iq = sqlite3.connect('proj2part3/LMS.db')
    
    iq_cur = iq.cursor()
    iq_cur.execute('''SELECT (SELECT Branch_name FROM LIBRARY_BRANCH LB WHERE BL.Branch_ID = LB.Branch_ID)
                    AS Branch_name, COUNT(*) AS no_of_copies_loaded FROM Book_Loans BL, BOOK B 
                    WHERE B.Book_ID=BL.Book_ID AND B.Title = ? GROUP BY Branch_ID''',
            (selection,))
    records = iq_cur.fetchall()

    print_braches = ''

    for branch in records:
        print_braches += str(branch[0]+ "\t" + str(branch[1]) + "\n")
    branch_label = tk.Label(tab4, text = print_braches)
    branch_label.grid(row = 1, column = 1, pady = 20, sticky = 'nw')

    
    iq.commit()
    iq.close()
#req 5
# search value
def days_find():
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()         

    iq = sqlite3.connect('proj2part3/LMS.db')
    
    iq_cur = iq.cursor()
    iq_cur.execute('''SELECT BI.Card_No, Days_Late_Return FROM BOOK_LOANS BL, vBOOKLoanInfo BI 
                    WHERE BL.Card_No=BI.Card_No AND BL.Due_date=BI.Due_date 
                    AND BI.Due_date >= DATE(?) AND BI.Due_date <= DATE(?) AND Late = 1''',
            (start_date,end_date,))
    records = iq_cur.fetchall()

    print_days = ''

    for day in records:
        print_days += str(str(day[0])+ "\t   " + str(int(day[1])) + "\n")
    days_label = tk.Label(tab5, text = print_days)
    days_label.grid(row = 1, column = 1, pady = 20, sticky = 'nw')

    
    iq.commit()
    iq.close()

#print book_list
def late_list():
    late_conn = sqlite3.connect('proj2part3/LMS.db')
    
    late_cur = late_conn.cursor()
    late_cur.execute("SELECT Due_date FROM BOOK_LOANS WHERE Late = 1 ORDER BY Due_date ASC")
    output_books = late_cur.fetchall()

    latebox = tk.Listbox(tab5)
    latebox.grid(row = 1, padx = 100, ipady = 30, ipadx = 30, sticky='nsew')
    
    for output_record in output_books:	
        latebox.insert(tk.END, output_record[0]) 

#print book_list
def book_list():
    book_conn = sqlite3.connect('proj2part3/LMS.db')
    
    book_cur = book_conn.cursor()
    book_cur.execute("SELECT DISTINCT Title FROM BOOK")
    output_books = book_cur.fetchall()

    listbox = tk.Listbox(tab4)
    listbox.grid(row = 1, column = 0, ipady = 100, ipadx = 30)
    
    for output_record in output_books:	
        listbox.insert(tk.END, output_record[0]) 

    return listbox
def submit6a():
    borrower_card_no = card_no_textbox_tab6.get()
    borrower_name = name_textbox_tab6.get()


    if borrower_card_no:
        query = "SELECT Card_No, Borrower_Name, LateFeeBalance FROM vBookLoanInfo WHERE Card_No = ? ORDER BY LateFeeBalance DESC"
        param = (borrower_card_no,)

    elif borrower_name:
        query = "SELECT Card_No, Borrower_Name, LateFeeBalance FROM vBookLoanInfo WHERE Borrower_Name LIKE ? ORDER BY LateFeeBalance DESC"
        param = ('%' + borrower_name + '%',)
    else:
        query = "SELECT Card_No, Borrower_Name, LateFeeBalance FROM vBookLoanInfo ORDER BY LateFeeBalance DESC"
        param = None
    
    with sqlite3.connect('proj2part3/LMS.db') as conn:
        cur = conn.cursor()
        if param:
            cur.execute(query, param)
        else:
            cur.execute(query)
        borrower_info = cur.fetchall()

    for row in borrower_info_tree.get_children():
        borrower_info_tree.delete(row)
    for row in borrower_info:
            card_no, borrower_name, late_fee_balance = row
            formatted_late_fee = "${:.2f}".format(late_fee_balance)
            borrower_info_tree.insert("", "end", values=(card_no, borrower_name, formatted_late_fee))


window = tk.Tk()

window.title("Library Management System")
window.geometry("700x700")

window.resizable(False, False)


notebook = tkrtk.Notebook(window)

# Create the home screen frame
home_screen = tk.Frame(window)

title = tk.Label(home_screen, text = "Library Management System", font =("Times", "30", "bold"))
subtitle = tk.Label(home_screen, text = "CSE 3330 - Database Systems and File Structures\nNadra Guizani\n", font =("Times", "15", "bold"))
utalogo = tk.PhotoImage(file="proj2part3/utalogo.png")
utalogo = utalogo.subsample(10)
utalabel = tk.Label(home_screen, image=utalogo)

# Create labels or buttons for each tab on the home screen
label1 = tk.Label(home_screen, text="Requirement 1:\nThe user checks out a book by inputting their card number, branch ID, and the requested book.")
label2 = tk.Label(home_screen, text="Requirement 2:\nThe user adds a new borrower to the LMS and is outputted their new card number.")
label3 = tk.Label(home_screen, text="Requirement 3:\nThe user adds a book by specifying its name and author, along with a publisher.")
label4 = tk.Label(home_screen, text="Requirement 4:\nThe user can choose a book, and then is outputted the number of copies loaned out per branch.")
label5 = tk.Label(home_screen, text="Requirement 5:\nThe user selects a date range and is given the books that were returned late along with late days.")
label6a = tk.Label(home_screen, text="Requirement 6a:\nThe user is able to search borrowers by specifying criteria in their search.")
label6b = tk.Label(home_screen, text="Requirement 6b:\nThe user searches book information by specifying criteria in their search.")


title.pack()
subtitle.pack()
utalabel.pack(side = "bottom")

# Add the labels or buttons to the home screen
label1.pack(pady=10)
label2.pack(pady=10)
label3.pack(pady=10)
label4.pack(pady=10)
label5.pack(pady=10)
label6a.pack(pady=10)
label6b.pack(pady=10)

label1.bind("<Button-1>", lambda e: switch_to_tab(1))
label2.bind("<Button-1>", lambda e: switch_to_tab(2))
label3.bind("<Button-1>", lambda e: switch_to_tab(3))
label4.bind("<Button-1>", lambda e: switch_to_tab(4))
label5.bind("<Button-1>", lambda e: switch_to_tab(5))
label6a.bind("<Button-1>", lambda e: switch_to_tab(6))
label6b.bind("<Button-1>", lambda e: switch_to_tab(7))


# Add the home screen frame as the first tab in the notebook
notebook.add(home_screen, text="Home")

# each tab

tab1 = tkrtk.Frame(notebook)
tab2 = tkrtk.Frame(notebook)
tab3 = tkrtk.Frame(notebook)
tab4 = tkrtk.Frame(notebook)
tab5 = tkrtk.Frame(notebook)
tab6a = tkrtk.Frame(notebook)
tab6b = tkrtk.Frame(notebook)

notebook.add(tab1, text = "Req. 1")
notebook.add(tab2, text = "Req. 2")
notebook.add(tab3, text = "Req. 3")
notebook.add(tab4, text = "Req. 4")
notebook.add(tab5, text = "Req. 5")
notebook.add(tab6a, text = "Req. 6a")
notebook.add(tab6b, text = "Req. 6b")

notebook.pack(fill = "both", expand = "yes")

# -----------------------------------------------------------------------------------------
tab1_label = tk.Label(tab1, text = "Check Out a Book", font=("Arial", 16, "bold"))
tab1_label.pack(pady = 15)
book_conn = sqlite3.connect('proj2part3/LMS.db')
book_cur = book_conn.cursor()

book_cur.execute("SELECT Title FROM BOOK")
output_books = book_cur.fetchall()

print_record =''
for output_record in output_books:	
    print_record += output_record[0] + "\n"

book_text = tk.LabelFrame(tab1, text = "Books", font = ("aerial", 14, "bold"))
book_text.pack(side = "left")
book_label = tk.Label(book_text, text = print_record, font = ("aerial", 12))
book_label.pack(side = "top")

enter_label = tk.LabelFrame(tab1, text = "Enter book to check out")
enter_label.pack(side = "top")
enter_textbox = tk.Entry(enter_label)
enter_textbox.pack(pady=5)

card_no_label = tk.LabelFrame(tab1, text = "Card no.")
card_no_label.pack(side = "top")
card_no_textbox = tk.Entry(card_no_label)
card_no_textbox.pack(pady=5)

branch_label = tk.LabelFrame(tab1, text = "Branch id:")
branch_label.pack(side = "top")
branch_textbox = tk.Entry(branch_label)
branch_textbox.pack(pady=5)


submit_btn = tk.Button(tab1, text = 'Check out', command = submit1)
submit_btn.pack(pady=5)

book_cur.execute("SELECT * FROM BOOK_COPIES")
output_book_copies = book_cur.fetchall()

print_record =''
for output_record in output_book_copies:	
    print_record += str(output_record[0]) +" " + str(output_record[1]) + \
                 " " + str(output_record[2]) + "\n"

book_copies_tree = tkrtk.Treeview(tab1, columns=("book_id", "branch_id", "no_of_copies"), show="headings")
book_copies_tree.column("book_id", width=100)
book_copies_tree.column("branch_id", width=100)
book_copies_tree.column("no_of_copies", width=100)
book_copies_tree.heading("book_id", text="Book ID")
book_copies_tree.heading("branch_id", text="Branch ID")
book_copies_tree.heading("no_of_copies", text="No. of Copies")
book_copies_tree.pack(side = "bottom")

display_book_copies()

message_label = tk.Label(tab1, text="", font=("Arial", 12))
message_label.pack()
# -----------------------------------------------------------------------------------------

tab2_label = tk.Label(tab2, text = "Requirement 2")

#define all the texboxes
Name = tk.Entry(tab2, width = 30)
Name.grid(row = 1, column = 1, padx=20)

Address = tk.Entry(tab2, width = 30)
Address.grid(row = 2, column = 1)

Phone = tk.Entry(tab2, width = 30)
Phone.grid(row = 3, column = 1)

#label
new_label = tk.Label(tab2, text = "Add a New Borrower", font = ("aerial", 16, "bold"))
new_label.grid(row = 0, columnspan = 2, pady = 10)

Name_label = tk.Label(tab2, text = 'Name: ')
Name_label.grid(row = 1, column = 0, padx=20)

Address_label = tk.Label(tab2, text = 'Address: ')
Address_label.grid(row = 2, column = 0)

Phone_label = tk.Label(tab2, text = 'Phone: ')
Phone_label.grid(row = 3, column = 0)

#submit button
submit_button = tk.Button(tab2, text = 'Add New Borrower', command = submit2)
submit_button.grid(row = 6, column = 1, columnspan = 2, pady = 10, padx = 10, ipadx = 5, sticky='e')

iq_button = tk.Button(tab2, text = 'See your Card#', command = input_query)
iq_button.grid(row = 7, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 100)
# -----------------------------------------------------------------------------------------
tab3_label = tk.Label(tab3, text = "Add New Book", font=("Arial", 16, "bold"))
tab3_label.pack(pady=15)

conn = sqlite3.connect('proj2part3/LMS.db')
c = conn.cursor()

# create labels and text boxes
title_label = tk.Label(tab3, text="Title")
title_label.pack()
title_entry = tk.Entry(tab3)
title_entry.pack()

publisher_label = tk.Label(tab3, text="Publisher")
publisher_label.pack()
publisher_entry = tk.Entry(tab3)
publisher_entry.pack()

author_label = tk.Label(tab3, text="Author")
author_label.pack()
author_entry = tk.Entry(tab3)
author_entry.pack()

error_label = tk.Label(tab3, text=f"")
error_label.pack()

def add_book_to_database():
    title = title_entry.get()
    publisher_name = publisher_entry.get()
    author_name = author_entry.get()
    branch_copies = 5

    # check if publisher exists
    c.execute("SELECT * FROM PUBLISHER WHERE Publisher_Name = ?", (publisher_name,))
    publisher = c.fetchone()
    if not publisher:
        error_label.config(text=f"Error: Publisher {publisher_name} does not exist!")
        return
    else:
        error_label.config(text=f"")

    # insert new book into BOOK table
    c.execute("INSERT INTO BOOK (Title, Publisher_name) VALUES (?, ?)", (title, publisher_name))
    book_id = c.lastrowid

    # insert new author into BOOK_AUTHORS table
    c.execute("INSERT INTO BOOK_AUTHORS (Book_Id, Author_Name) VALUES (?, ?)", (book_id, author_name))

    # insert 5 copies of the book into each branch
    c.execute("SELECT Branch_Id FROM LIBRARY_BRANCH")
    branches = c.fetchall()
    for branch_id in branches:
        c.execute("INSERT INTO BOOK_COPIES (Book_Id, Branch_Id, No_Of_Copies) VALUES (?, ?, ?)",
                    (book_id, branch_id[0], branch_copies))
        # print(f"Added {branch_copies} copies of book {book_id} to branch {branch_id[0]}")

    conn.commit()

    title_entry.delete(0, tk.END)
    publisher_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)



    success_label = tk.Label(tab3, text="Book " + title + " added successfully.")
    # success_label.grid(row=4, columnspan=2)
    success_label.pack()

# create button
add_button = tk.Button(tab3, text="Add Book", command=add_book_to_database)
add_button.pack()

# -----------------------------------------------------------------------------------------
tab4_label = tk.Label(tab4, text = "Requirement 4")
#label
books_label = tk.Label(tab4, text = "Book List", font = ("Aerial","14","bold"))
books_label.grid(row = 0, column = 0, sticky='nsew')
listbox = book_list()

result_label = tk.Label(tab4, text = "Result", font = ("Aerial","14","bold"))
result_label.grid(row = 0, column = 1, sticky='nw')

Branches_label = tk.Label(tab4, text = "Branch Name" + "   " + "Number of Copies", font = ("Aerial", "14", "underline"))
Branches_label.grid(row = 1, column = 1, sticky='nw')


#submit button
searches_button = tk.Button(tab4, text = 'Search', command = lambda: search(listbox))
searches_button.grid(row = 2, column = 0, pady = 10, sticky = 'e')
# -----------------------------------------------------------------------------------------


# tab5_label = tk.Label(tab5, text = "Late Day Search", font = ("Aerial", "14", "bold"))
# tab5_label.grid(row = 0, column = 0)
#define all the texboxes
start_date_entry = tk.Entry(tab5, width = 10)
start_date_entry.grid(row = 3, column = 0)

end_date_entry = tk.Entry(tab5, width = 10)
end_date_entry.grid(row = 6, column = 0)


#label
date_list = tk.Label(tab5, text = "Due_dates_late")
date_list.grid(row = 0,column = 0)
late_list()

start_label = tk.Label(tab5, text = "Start_dates (yyyy-mm-dd)")
start_label.grid(row = 2,column = 0)
to_label = tk.Label(tab5, text = "to")
to_label.grid(row = 4,column = 0, pady= 5)
end_label = tk.Label(tab5, text = "End_dates (yyyy-mm-dd)")
end_label.grid(row = 5,column= 0,padx=10)

output_label = tk.Label(tab5, text = "Result")
output_label.grid(row = 0, column=1)

date_label = tk.Label(tab5, text = "Card_No" + "   " + "Days_of_late")
date_label.grid(row = 1,column=1,  sticky='n')


#find button
Find_button = tk.Button(tab5, text = 'Find', command = days_find)
Find_button.grid(row = 7, column = 0, pady = 10)

# -----------------------------------------------------------------------------------------

tab6_label = tk.Label(tab6a, text="Borrower Search", font=("Arial", 16, "bold"))
tab6_label.pack(side="top", pady = 10)

name_frame = tk.Frame(tab6a)
name_frame.pack(pady=10)
name_label = tk.Label(name_frame, text="Name:")
name_label.pack(side="left")
name_textbox_tab6 = tk.Entry(name_frame)  # Renamed name_textbox to name_textbox_tab6
name_textbox_tab6.pack(side="left")

card_no_frame = tk.Frame(tab6a)
card_no_frame.pack(pady=10)
card_no_label = tk.Label(card_no_frame, text="Card No.:")
card_no_label.pack(side="left")
card_no_textbox_tab6 = tk.Entry(card_no_frame)  # Renamed card_no_textbox to card_no_textbox_tab6
card_no_textbox_tab6.pack(side="left")

search_button = tk.Button(tab6a, text="Search", command = submit6a)
search_button.pack()

borrower_info_tree = tkrtk.Treeview(tab6a, columns=("card_no", "borrower_name", "late_fee_balance"), show="headings")
borrower_info_tree.column("card_no", width=100)
borrower_info_tree.column("borrower_name", width=200)
borrower_info_tree.column("late_fee_balance", width=100)
borrower_info_tree.heading("card_no", text="Card No.")
borrower_info_tree.heading("borrower_name", text="Borrower Name")
borrower_info_tree.heading("late_fee_balance", text="Late Fee Balance")
borrower_info_tree.pack()

# -----------------------------------------------------------------------------------------

# Create the search label and text box
tab6b_label = tk.Label(tab6b, text = "Book Search", font=("Arial", 16, "bold"))
tab6b_label.pack(pady=10)

search_label = tk.Label(tab6b, text="Enter a filter for book search (book id, book title, part of book title): ")
search_label.pack()
search_criteria = tk.StringVar()
search_box = tk.Entry(tab6b, width=30, textvariable=search_criteria)
search_box.pack()

# Modifying the vBookLoanInfo view to have Book_Id since the requirement is to search by Book_Id
c.execute("""DROP VIEW IF EXISTS vBookLoanInfo2""")
c.execute("""CREATE VIEW IF NOT EXISTS vBookLoanInfo2 AS
             SELECT
               B.Book_Id,
               (julianday(BL.Returned_Date) - julianday(BL.Date_out)) AS TotalDays,
               B.Title AS Book_Title,
               BL.Card_No,
               BR.Name AS Borrower_Name,
               BL.Date_Out,
               BL.Due_Date,
               BL.Returned_Date,
               (julianday(BL.Returned_Date) - julianday(BL.Due_Date)) * CASE
                WHEN BL.Returned_Date > BL.Due_Date THEN 1
                ELSE 0
               END AS Days_Late_Return,
               LB.Branch_ID,
               LB.LateFee * CASE WHEN Returned_Date > Due_Date
                THEN LateFee
                ELSE 0
                END AS LateFeeBalance
             FROM Book B
             LEFT JOIN Book_loans BL ON B.Book_id = BL.Book_id
             LEFT JOIN Library_branch LB ON BL.Branch_id = LB.Branch_id
             LEFT JOIN BORROWER BR ON BL.Card_no = BR.Card_no;""")
conn.commit()

no_results_label = tk.Label(tab6b, text="")
no_results_label.pack()

# Define a function to execute the book search query and display the results
def list_books():

    # Remove the previous table
    for widget in tab6b.winfo_children():
        if isinstance(widget, tkrtk.Treeview):
            widget.destroy()

    # Get the search criteria from the user
    criteria = search_criteria.get()

    if not criteria:
        # If no search criteria was provided, order the results by the highest late fee
        c.execute("""SELECT Book_Id, Book_Title, Card_No, Borrower_Name, Date_Out, Due_Date, Returned_Date,
                            TotalDays, Days_Late_Return, Branch_ID, 
                            CASE WHEN LateFeeBalance IS NOT NULL THEN '$' || ROUND(LateFeeBalance, 2) ELSE 'Non-Applicable' 
                            END AS Late_Fee
                     FROM vBookLoanInfo2
                     ORDER BY LateFeeBalance DESC""")
    else:
        # If search criteria was provided, filter the results accordingly
        c.execute("""SELECT Book_Id, Book_Title, Card_No, Borrower_Name, Date_Out, Due_Date, Returned_Date,
                            TotalDays, Days_Late_Return, Branch_ID, 
                            CASE WHEN LateFeeBalance IS NOT NULL THEN '$' || ROUND(LateFeeBalance, 2) ELSE 'Non-Applicable' 
                            END AS Late_Fee
                     FROM vBookLoanInfo2
                     WHERE Book_Title LIKE ? OR Book_Title LIKE ? OR Book_Id=?
                     ORDER BY LateFeeBalance DESC""", (f"%{criteria}%", f"%{criteria}%", criteria))
    results = c.fetchall()

    if not results:
        # If no results were found, display a message to the user
        no_results_label.config(text=f"No books found.")
        return 

    else:
        no_results_label.config(text=f"")

        # If results were found, create a table to display them
        columns = ("Book Id", "Book Title", "Card Number", "Borrower Name", "Date Out", "Due Date", "Returned Date", 
                "Total Days", "Days Late Return", "Branch ID", "Late Fee")

        table = tkrtk.Treeview(tab6b)
        table.pack(fill=tk.BOTH, expand=1)
        table.column("#0", width=0)

        # Set up the table columns and headings
        table["columns"] = columns
        for col in columns:
            table.heading(col, text=col)
            table.column(col, width=100)
        
        # Fetch and display the results
        for i, row in enumerate(results):
            cur_row = list(row)
            if cur_row[10][-2] == ".": # to handle .5, .0, etc.
                cur_row[10] = f"{cur_row[10]}0"

            table.insert("", "end", text="", values=cur_row)

    conn.commit()
    
# Create the search button
search_button = tk.Button(tab6b, text="Search", command=list_books)
search_button.pack()

tk.mainloop()

