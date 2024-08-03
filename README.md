 # Library Management System
 ## README
 

*Ensure that you have Python installed on your machine. If not, download and install
Python version 3.11 from the official Python website (www.python.org).*

*The code uses the Tkinter package for GUI, which is typically included with
Python installations. However, if you don't have Tkinter installed, you may need to install it separately. You can install Tkinter using pip:* `pip install tkinter`.

*The GUI will also connect to an SQLite3 backend, which is preinstalled with Python. If it is not, you can install SQLite3 with* `pip3 install sqlite3`.


### Instructions on how to run the application and GUI:
* Download the code, `Library-Management-System` is the parent directory
* Verify that `LMS.db` is stored within the ‘proj2part3’ directory.
* Run the Library Management System Database GUI by using the command:
```
python LMSApplication.py
```

### Components

#### Home:
* This screen is the main screen. It contains the title and lists a brief description of each requirement. Clicking each requirement will navigate the user to that screen.
* There is also a tab view that contains a tab for each requirement. Click each tab (Req. 1, Req. 2., etc.) to navigate to the requirement.

#### Requirement 1:
* To check out a book, enter the name of the book that is listed on the left of the screen. Enter a 6 digit card number, and the branch ID from the table below.
* Click “Check out”
* Upon successful checkout, the application will display the borrower’s name and “successfully checked out” with the book’s name.

![Req1](https://github.com/AMahouch/Library-Management-System/assets/97981126/343be6e5-b05e-44c7-85f1-4ea403270a3a)


#### Requirement 2:
* To add a new borrower, enter the name, the address, and the phone number.
* Click “Add New Borrower”. It will automatically assign a card #.
* Click “See your Card#” to see the card number.
* The application will display the related card number.

![Req2](https://github.com/AMahouch/Library-Management-System/assets/97981126/a7c1cf94-ddd3-4d22-9180-0bdbd5c7b93f)



#### Requirement 3:
* Enter book name, publisher name (must be an existing publisher), author name.
* Push “Add book”
* A successful addition will display “Book added successfully.”
* A failed addition with invalid (non-existing) publisher name will display “Error: Publisher {publisher_name} does not exist!”

![Req3](https://github.com/AMahouch/Library-Management-System/assets/97981126/65d3efbc-38c5-4b9b-b762-da9f36ebef30)



#### Requirement 4:
* Choose a book name on the “Book List”
* Click “Search”.
* The program will display branch names and the number of the book loaned out from the branch.

![Req4](https://github.com/AMahouch/Library-Management-System/assets/97981126/d08791d7-e4b1-4a01-b11c-d6f61ac8b4c8)


#### Requirement 5:
* Due_dates_late shows a list of dates which have returned the book late.
*  Enter the start date and end date you want to search for information.
* Click “Find”.
* The program shows the card numbers of people who are in between those dates and how late they returned the book.

![Req5](https://github.com/AMahouch/Library-Management-System/assets/97981126/f312b7be-5a74-43f8-906d-57ce493a6f4d)



#### Requirement 6a:
* There are 2 text entry fields, one for Name and one for Card number.
* The user can enter a part of a name or the full name and press “Search”, which will display the card numbers, name, and late fee balance of the filtered criteria in the table below.
* The same logic is applied with the card number entry, except the user has to enter in the entire card number and press “Search”
* If the user wishes not to enter any criteria, they may leave the text fields blank andpress “Search”, showing all borrowers sorted by their late fee balance.

![Req6a](https://github.com/AMahouch/Library-Management-System/assets/97981126/85673203-d240-437b-9dc7-af3226a58ec5)


#### Requirement 6b:

* Enter book id, book title or part of book title.
* Push “search”
* Table of the view (Book Id, Book Title, Card Number, Borrower Name, Date Out, Due Date, Returned Date, Total Days, Days Late Return, Branch ID, Late Fee), ordered by descending late fee, will display according to the search filter.
* If nothing is entered in the search filter, table of the view (Book Id, Book Title, Card Number, Borrower Name, Date Out, Due Date, Returned Date, Total Days, Days Late Return, Branch ID, Late Fee), ordered by descending late fee, will display of all books.
* Failed search with invalid (non-existing) book id, book title or part of book title will display “No books found.”

![Req6b](https://github.com/AMahouch/Library-Management-System/assets/97981126/659a492f-b0e4-483d-bd63-4a70f328a7c8)

