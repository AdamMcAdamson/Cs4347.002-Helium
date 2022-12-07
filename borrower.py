import sqlite3 as sql
from flask import request
from flask_restful import Resource

from consts import DB_FILE, SEARCH_PAGE_SIZE, CHECKOUT_LIMIT

class BorrowerCreate(Resource):

    def post(self):
        args = {'ssn':request.args.get('ssn', ''), 'bname':request.args.get('name', ''), 'address':request.args.get('address', ''), 'phone':request.args.get('phone', 'NULL')}

        with sql.connect(DB_FILE) as conn:
            conn.row_factory = sql.Row
            c = conn.cursor()
            
            # Check for existing SSN and return useful error if it already exists
            if c.execute("SELECT * FROM BORROWER WHERE Ssn = :ssn", args).fetchone():
                return {"message": "Only one borrower card per person. Ssn must be unique."}, 409
            
            # Create borrower
            command = "INSERT INTO BORROWER (Ssn, Bname, Address, Phone) VALUES (:ssn, :bname, :address, :phone);"
            c.execute(command, args)

            card_id = c.execute("SELECT Card_id FROM BORROWER WHERE Ssn = :ssn", args).fetchone()["Card_id"]
            return {"message": "Borrower Successfully Created. Card ID: " + 'ID{:0>6}'.format(str(card_id)) + ".", "card_id_str": 'ID{:0>6}'.format(str(card_id)), "card_id_num": card_id}, 200