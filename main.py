from flask import Flask, request
from flask_restful import Resource, Api
import sqlite3 as sql
import traceback, sys

import consts
from search import Search

app = Flask(__name__, static_url_path='/')
api = Api(app)

def index(): 
    return app.send_static_file('index.html')

app.add_url_rule('/', 'index', index)


#TODO: refactor as a Resource put method
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

app.add_url_rule('/borrower/create', 'create_borrower', create_borrower, methods=["POST"])


api.add_resource(Search, '/search', endpoint='search')


if __name__ == '__main__':
    with sql.connect(DB_FILE) as conn:
        file = open('./resources/schema.sql', mode = 'r', encoding='utf-8')
        c = conn.cursor()
        c.executescript(file.read())
    app.run(debug=True)