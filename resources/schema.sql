 
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
    
	INSERT INTO BOOK (Isbn, Title)
	VALUES ("0195153448", "Classical Mythology")
	VALUES ("0002005018", "Clara Callan: A Novel")
	VALUES ("0060973129", "Decision In Normandy")
	VALUES ("0374157065", "Flu: The Story Of The Great Influenza Pandemic Of 1918 And The Search For The Virus That Caused It")
	VALUES ("0393045218", "The Mummies Of Urumchi")
	VALUES ("0399135782", "The Kitchen God's Wife")
	VALUES ("0425176428", "What If?: The World's Foremost Military Historians Imagine What Might Have Been")
	VALUES ("0671870432", "Pleading Guilty")
	VALUES ("0679425608", "Under The Black Flag: The Romance And The Reality Of Life Among The Pirates")
	VALUES ("074322678X", "Where You'll Find Me: And Other Stories");

	INSERT INTO AUTHORS (Isbn, Title)
	VALUES (0, "Mark P. O. Morford")
	VALUES (1, "Robert J. Lenardon")
	VALUES (2, "Richard Bruce Wright")
	VALUES (3, "Carlo D'Este")
	VALUES (4, "Gina Kolata")
	VALUES (5, "Elizabeth Wayland Barber")
	VALUES (6, "E. J. W. Barber")
	VALUES (7, "Amy Tan")
	VALUES (8, "Robert Cowley")
	VALUES (9, "Scott Turow")
	VALUES (10, "Stacy Keach")
	VALUES (11, "David Cordingly")
	VALUES (12, "Ann Beattie");

	INSERT INTO BOOK_AUTHORS (Isbn, Title)
	VALUES (0, "0195153448")
	VALUES (1, "0195153448")
	VALUES (2, "0002005018")
	VALUES (3, "0060973129")
	VALUES (4, "0374157065")
	VALUES (5, "0393045218")
	VALUES (6, "0393045218")
	VALUES (7, "0399135782")
	VALUES (8, "0425176428")
	VALUES (9, "0671870432")
	VALUES (10, "0671870432")
	VALUES (11, "0679425608")
	VALUES (12, "074322678X");
