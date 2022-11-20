from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import sqlite3 as sql
import traceback, sys

DB_FILE = 'HeliumDB.db'
SEARCH_PAGE_SIZE = 20

app = Flask(__name__, static_url_path='/')
api = Api(app)

def index(): 
    return app.send_static_file('index.html')

app.add_url_rule('/', 'index', index)

with sql.connect(DB_FILE) as conn:
    file = open('./resources/schema.sql', mode = 'r', encoding='utf-8')
    c = conn.cursor()
    c.executescript(file.read())


class Quote(Resource):
    def get(self):
        args = request.args
        with sql.connect(DB_FILE) as conn:
            conn.row_factory = sql.Row
            c = conn.cursor()
            #return jsonify({"message": 200, "success":True, "data": [dict(x) for x in (c.execute('SELECT * FROM quote').fetchall())]})
            return [dict(x) for x in (c.execute('SELECT * FROM quote').fetchall())]


class Search(Resource):

    def get(self):
        args = {'q':request.args.get('q', '').lower()}

        with sql.connect(DB_FILE) as conn:
            #ISBN
            #Book title
            #Book author(s)
            #Book availability (is the book currently checked out?)
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
            ;
            '''

            return [dict(x) for x in c.execute(sql_query, args).fetchmany(size=SEARCH_PAGE_SIZE)]


def create_borrower():
    args = request.args

    ssn = args.get("ssn")
    bname = args.get("bname")
    address = args.get("address")
    phone = args.get("phone", "NULL")

    stuff = "SSN: " + ssn + "\tBNAME: " + bname + "\tADDRESS: " + address + "\tPHONE: " + phone
    return stuff,203
    with sql.connect(DB_FILE) as conn:
        conn.row_factory = sql.Row
        c = conn.cursor()
        # @TODO: Check for existing SSN and return useful error if it already exists
        # command = "INSERT INTO BORROWER (Ssn, Bname, Address, Phone) VALUES VALUES (?, ?, ?, ?);",
        # c.execute(
        #     command,
        #     (ssn, bname, address, phone)
        # )
        # + borrower[0] + "', '" + borrower[1] + "', '" + borrower[2]+ "', '" + borrower[3] + "')"        
        # return [dict(x) for x in (c.execute('SELECT * FROM quote').fetchall())]
        return app.make_response(200)


api.add_resource(Quote, '/quote', endpoint='quote')
api.add_resource(Search, '/search', endpoint='search')

app.add_url_rule('/borrower/create', 'create_borrower', create_borrower, methods=["POST"])

if __name__ == '__main__':
    app.run(debug=True)