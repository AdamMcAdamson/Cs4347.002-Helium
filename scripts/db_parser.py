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

        books.append([line["ISBN10"], line["Title"], "https://images.isbndb.com/covers/" + line["ISBN13"][9:11] + "/" + line["ISBN13"][11:] + "/" + line["ISBN13"] + ".jpg"])
        
        for j in line["Author"].split(','):
            if j in authors:
                index = authors.index(j)
                book_author = [index, line["ISBN10"]]
                if book_author not in book_authors:
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

    header = '''DROP TABLE IF EXISTS BOOK;

CREATE TABLE BOOK (
    Isbn CHAR(10) PRIMARY KEY,
    Title VARCHAR NOT NULL,
    Cover_url VARCHAR NOT NULL
);

DROP TABLE IF EXISTS AUTHORS;

CREATE TABLE AUTHORS (
    Author_id INTEGER PRIMARY KEY AUTOINCREMENT,
    Name VARCHAR NOT NULL
);

DROP TABLE IF EXISTS BOOK_AUTHORS;

CREATE TABLE BOOK_AUTHORS (
    Author_id INTEGER NOT NULL,
    Isbn CHAR(10) NOT NULL,
    PRIMARY KEY (Author_id, Isbn),
    FOREIGN KEY (Author_id) REFERENCES AUTHORS (Author_id),
    FOREIGN KEY (Isbn) REFERENCES BOOK (Isbn)
);

DROP TABLE IF EXISTS BORROWER;

CREATE TABLE BORROWER (
    Card_id INTEGER PRIMARY KEY AUTOINCREMENT,
    Ssn CHAR(11) NOT NULL UNIQUE,
    Bname VARCHAR NOT NULL,
    Address VARCHAR NOT NULL,
    Phone CHAR(14)
);
'''

    file.write(header)

    # Populate BOOK Table
    file.write("\nINSERT INTO BOOK (Isbn, Title, Cover_url)\n\tVALUES")
    for book in books[:-1]:
        file.write("\n\t\t('" + book[0] + "', '" + book[1] + "', '" + book[2] + "'),")
    file.write("\n\t\t('" + books[-1][0] + "', '" + books[-1][1] + "', '" + books[-1][2] + "');\n")

    # Populate AUTHORS Table
    file.write("\nINSERT INTO AUTHORS (Name)\n\tVALUES")
    for author in authors[:-1]:
        file.write("\n\t\t('" + author + "'),")
    file.write("\n\t\t('" + authors[-1] + "');\n")

    # Populate BOOK_AUTHORS Table
    file.write("\nINSERT INTO BOOK_AUTHORS (Author_id, Isbn)\n\tVALUES")
    for book_author in book_authors[:-1]:
        file.write("\n\t\t(" + str(book_author[0]) + ", '" + book_author[1] + "'),")
    file.write("\n\t\t(" + str(book_authors[-1][0]) + ", '" + book_authors[-1][1] + "');\n")

    # Populate BORROWER Table
    file.write("\nINSERT INTO BORROWER (Ssn, Bname, Address, Phone)\n\tVALUES")
    for borrower in borrowers[:-1]:
        file.write("\n\t\t('"+ borrower[0] + "', '" + borrower[1] + "', '" + borrower[2]+ "', '" + borrower[3] + "'),")
    file.write("\n\t\t('"+ borrowers[-1][0] + "', '" + borrowers[-1][1] + "', '" + borrowers[-1][2]+ "', '" + borrowers[-1][3] + "');\n")
        
