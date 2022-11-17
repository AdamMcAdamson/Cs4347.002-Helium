import csv
import sqlite3 as sql

with open('./resources/books.csv', mode = 'r') as file:

    csvFile = csv.reader(file, delimiter='\t')
    authors = []
    books = []
    book_authors = []

    headers = next(csvFile)
    for i in range(10):
        line = next(csvFile)
        line = dict(zip(headers, line))
        
        books.append([line["ISBN10"], line["Title"]])
        
        for j in line["Author"].split(','):
            if j in authors:
                index = authors.index(j)
                book_authors.append([index, line["ISBN10"]])
            else:
                authors.append(j)
                book_authors.append([len(authors)-1, line["ISBN10"]])

with open('./resources/schema.sql', mode = 'w+') as file:
    header = '''
    CREATE TABLE BOOK (
        Isbn CHAR(10) NOT NULL,
        Title VARCHAR NOT NULL,
        PRIMARY KEY (Isbn) 
    );

    CREATE TABLE AUTHORS (
        Author_id INT NOT NULL,
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
    '''

    file.write(header)

    # Populate BOOK Table
    file.write("\n\tINSERT INTO BOOK (Isbn, Title)")
    for book in books:
        file.write('\n\tVALUES ("' + book[0] + '", "' + book[1] + '")')
    file.write(";\n")

    # Populate AUTHOR Table
    file.write("\n\tINSERT INTO AUTHORS (Isbn, Title)")
    for i, author in enumerate(authors):
        file.write('\n\tVALUES (' + str(i) + ', "' + author + '")')
    file.write(";\n")

    # Populate BOOK_AUTHORS Table
    file.write("\n\tINSERT INTO BOOK_AUTHORS (Isbn, Title)")
    for book_author in book_authors:
        file.write('\n\tVALUES (' + str(book_author[0]) + ', "' + book_author[1] + '")')
    file.write(";\n")
        
