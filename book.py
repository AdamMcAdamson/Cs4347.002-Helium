import sqlite3 as sql
from flask import request, make_response
from flask_restful import Resource

from consts import DB_FILE, SEARCH_PAGE_SIZE, CHECKOUT_LIMIT

# @TODO: Book availability
class Search(Resource):

    def get(self):
        args = {'q':request.args.get('q', '').lower(), 'p':request.args.get('p', ''), 's':SEARCH_PAGE_SIZE}

        with sql.connect(DB_FILE) as conn:
            conn.row_factory = sql.Row
            c = conn.cursor()

            sql_query = '''
            WITH q_authors AS (
                SELECT GROUP_CONCAT(Name,', ') AS Author_names, Isbn
                FROM AUTHORS NATURAL JOIN BOOK_AUTHORS
                GROUP BY Isbn
            )
            SELECT Isbn, Title, Author_names, Cover_url
            FROM BOOK NATURAL JOIN q_authors
            WHERE INSTR(LOWER(Title), :q) > 0
            OR INSTR(LOWER(Author_names), :q) > 0
            OR INSTR(LOWER(Isbn), :q) > 0
            ORDER BY INSTR(LOWER(Isbn), :q), INSTR(LOWER(Author_names), :q), INSTR(LOWER(Title), :q)
            LIMIT :s OFFSET (:p-1)*:s
            ;
            '''

            return [dict(x) for x in c.execute(sql_query, args).fetchmany(size=SEARCH_PAGE_SIZE)]

class Checkout(Resource):

    def post(self):
        args = {'isbn':request.args.get('isbn', ''), 'card_id':request.args.get('card_id', '')}

        if args['isbn'] == '' or args['card_id'] == '':
            return make_response("Bad Request. Missing query parameters (isbn, card_id).", 400)

        with sql.connect(DB_FILE) as conn:
            conn.row_factory = sql.Row
            c = conn.cursor()

            if dict(c.execute('SELECT COUNT(*) AS count FROM BOOK WHERE Isbn == :isbn', args).fetchone())['count'] != 1:
                return make_response("Unknown book.", 400)

            # @TODO: Update count check to number of copies of book available (should we want to support this)
            if dict(c.execute('SELECT COUNT(*) AS count FROM BOOK_LOANS WHERE Isbn == :isbn AND Date_in IS NULL', args).fetchone())['count'] >= 1:
                return make_response("The requested book is unavailable.", 409)

            if dict(c.execute('SELECT COUNT(*) AS count FROM BOOK_LOANS WHERE Card_id == :card_id AND Date_in IS NULL', args).fetchone())['count'] >= CHECKOUT_LIMIT:
                return make_response("Borrower has too many books checked out.", 409)

            sql_query = "INSERT INTO BOOK_LOANS (Isbn, Card_id) VALUES (:isbn, :card_id)"
            c.execute(sql_query, args)

            print(dict(c.execute('SELECT COUNT(*) AS count, isbn, Date_in FROM BOOK_LOANS GROUP BY Isbn', ()).fetchone()))

            return make_response("Book successfully checked out.", 200)


class Checkin(Resource):

    def get(self):
        args = {'q':request.args.get('q', '').lower(), 'p':request.args.get('p', ''), 's':SEARCH_PAGE_SIZE}

        with sql.connect(DB_FILE) as conn:
            conn.row_factory = sql.Row
            c = conn.cursor()

            sql_query = '''
            SELECT Loan_id, Isbn, Card_id, Date_out, Due_date, BName
            FROM BOOK_LOANS NATURAL JOIN BORROWER
            WHERE INSTR(LOWER(BName), :q) > 0
            OR INSTR(LOWER(Card_id), :q) > 0
            OR INSTR(LOWER(Isbn), :q) > 0
            ORDER BY INSTR(LOWER(BName), :q), INSTR(LOWER(Card_id), :q), INSTR(LOWER(Isbn), :q)
            LIMIT :s OFFSET (:p-1)*:s
            ;
            '''

            return [dict(x) for x in c.execute(sql_query, args).fetchmany(size=SEARCH_PAGE_SIZE)]

    def post(self):
        args = {'loan_id':request.args.get('loan_id', '')}

        if args['loan_id'] == '':
            return make_response("Bad Request. Missing query parameters (loan_id).", 400)


        with sql.connect(DB_FILE) as conn:
            conn.row_factory = sql.Row
            c = conn.cursor()

            if dict(c.execute('SELECT COUNT(*) AS count FROM BOOK_LOANS WHERE Loan_id == :loan_id AND Date_in IS NOT NULL', args).fetchone())['count'] == 1:
                return make_response("Book is already returned.", 409)

            sql_query = '''
            UPDATE BOOK_LOANS
            SET Date_in = CURRENT_DATE
            WHERE Loan_id == :loan_id
            '''

            c.execute(sql_query, args)
            
            return make_response("Book successfully checked in.", 200)




