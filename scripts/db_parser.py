import csv
import sqlite3 as sql

# Books File
authors = []
books = []
book_authors = []

# Borrowers File
borrowers = []
book_loans = []
fines = []

# Read and Parse Books file
with open('./resources/books.csv', mode = 'r', encoding='utf-8') as file:

    csvFile = csv.reader(file, delimiter='\t')

    headers = next(csvFile)

    for row in csvFile:
        line = dict(zip(headers, row))

        # Sanitize quotes (escape single quotes)
        line["Title"] = line["Title"].replace("'", "''")
        line["Author"] = line["Author"].replace("'", "''")
        line["Publisher"] = line["Publisher"].replace("'", "''")

        # Sanitize Symbols
        line["Title"] = line["Title"].replace("&amp;", "&")#.replace("&gt;", ">").replace("&lt;", "<")
        line["Title"] = line["Title"].replace("&gt;", ">")
        line["Title"] = line["Title"].replace("&lt;", "<")

        line["Author"] = line["Author"].replace("&amp;", "&")#.replace("&gt;", ">").replace("&lt;", "<")
        line["Author"] = line["Author"].replace("&gt;", ">")
        line["Author"] = line["Author"].replace("&lt;", "<")

        line["Publisher"] = line["Publisher"].replace("&amp;", "&")#.replace("&gt;", ">").replace("&lt;", "<")
        line["Publisher"] = line["Publisher"].replace("&gt;", ">")
        line["Publisher"] = line["Publisher"].replace("&lt;", "<")

        # @TODO: Add Book Cover_url

        books.append([line["ISBN10"], line["Title"], "https://images.isbndb.com/covers/" + line["ISBN13"][9:11] + "/" + line["ISBN13"][11:] + "/" + line["ISBN13"] + ".jpg"])
        
        for j in line["Author"].split(','):
            if j in authors:
                index = authors.index(j)
                book_authors.append([index, line["ISBN10"]])
            else:
                authors.append(j)
                # Author ID is 1 indexed in database
                book_authors.append([len(authors), line["ISBN10"]])

# Read and Parse Borrowers file
with open('./resources/borrowers.csv', mode = 'r', encoding='utf-8') as file:

    csvFile = csv.reader(file, delimiter=',')

    headers = next(csvFile)
    
    for row in csvFile:
        line = dict(zip(headers, row))

        # Currently ignoring: line["ID0000id"]
        borrowers.append([line["ssn"], (line["first_name"] + " " + line["last_name"]), (line["address"] + " " + line['city'] + ", " + line["state"]), line["phone"]])
        
# Write Schema File
with open('./resources/schema.sql', mode = 'w+', encoding='utf-8') as file:

    # @TODO: Add Book Cover_url Attribute
    header = '''
    CREATE TABLE BOOK (
        Isbn CHAR(10) NOT NULL,
        Title VARCHAR NOT NULL,
        Cover_url VARCHAR NOT NULL,
        PRIMARY KEY (Isbn) 
    );

    CREATE TABLE AUTHORS (
        Author_id INT NOT NULL AUTOINCREMENT,
        Name VARCHAR NOT NULL,
        PRIMARY KEY (Author_id) 
    );

    CREATE TABLE BOOK_AUTHORS (
        Author_id INT NOT NULL,
        Isbn CHAR(10) NOT NULL,
        PRIMARY KEY (Author_id, Isbn),
        FOREIGN KEY (Author_id) REFERENCES AUTHORS(Author_id),
        FOREIGN KEY (Isbn) REFERENCES BOOK(Isbn)
    );

    CREATE TABLE BORROWER (
        Card_id INT NOT NULL AUTOINCREMENT,
        Ssn CHAR(11) NOT NULL UNIQUE,
        Bname VARCHAR NOT NULL,
        Address VARCHAR NOT NULL,
        Phone CHAR(14),
        PRIMARY KEY (Card_id)
    );
    '''

    file.write(header)

    # Populate BOOK Table
    file.write("\n\tINSERT INTO BOOK (Isbn, Title)")
    for book in books:
        file.write("\n\tVALUES ('" + book[0] + "', '" + book[1] + "', '" + book[2] + "')")
    file.write(";\n")

    # Populate AUTHORS Table
    file.write("\n\tINSERT INTO AUTHORS (Name)")
    for author in authors:
        file.write("\n\tVALUES ('" + author + "')")
    file.write(";\n")

    # Populate BOOK_AUTHORS Table
    file.write("\n\tINSERT INTO BOOK_AUTHORS (Author_id, Isbn)")
    for book_author in book_authors:
        file.write("\n\tVALUES (" + str(book_author[0]) + ", '" + book_author[1] + "')")
    file.write(";\n")

    # Populate BORROWER Table
    file.write("\n\tINSERT INTO BORROWER (Ssn, Bname, Address, Phone)")
    for borrower in borrowers:
        file.write("\n\tVALUES ('"+ borrower[0] + "', '" + borrower[1] + "', '" + borrower[2]+ "', '" + borrower[3] + "')")
    file.write(";\n")
        
