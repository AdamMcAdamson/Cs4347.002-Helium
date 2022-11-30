import sqlite3 as sql
from flask import request
from flask_restful import Resource

from consts import DB_FILE#, SEARCH_PAGE_SIZE

class FinesPayment(Resource):

    def put(self):

        args = {'loan_id':request.args.get('loan_id', '')}

        with sql.connect(DB_FILE) as conn:
            conn.row_factory = sql.Row
            c = conn.cursor()

            sql_query = '''
            UPDATE (FINES NATURAL JOIN BOOK_LOANS)
            SET Paid = 1
            WHERE Date_in IS NOT NULL
            RETURNING *;
            '''

            ret = c.execute(sql_query).fetchone()
            if ret != flask:
                return "Successfully paid fine for loan {loan_id}".format(args), 200
            else:
                return "Could not pay fine for loan {loan_id}, make sure the book has been returned".format(args), 409

        return 

class FinesAll(Resource):

    # @TODO: Pagination or no?
    def get(self):

        with sql.connect(DB_FILE) as conn:
            conn.row_factory = sql.Row
            c = conn.cursor()

            sql_query = '''SELECT * FROM FINES;'''

            return [dict(x) for x in c.execute(sql_query).fetchall()]
            
class FinesUpdate(Resource):
    
    def put(self):

        with sql.connect(DB_FILE) as conn:
            conn.row_factory = sql.Row
            c = conn.cursor()

            # Not existing fines
            # --------------------------------------
            
            # book not returned
            get_new_fines_query = '''
            SELECT Loan_id
            FROM BOOK_LOANS LEFT JOIN FINES ON Loan_id
            WHERE Paid IS NULL AND Date_in IS NULL AND DATE(CURRENT_DATE) > Due_date;
            '''

            new_fines = [dict(x) for x in c.execute(get_new_fines_query).fetchall()]

            # book returned
            get_new_returned_fines_query = '''
            SELECT Loan_id
            FROM BOOK_LOANS LEFT JOIN FINES ON Loan_id
            WHERE Paid IS NULL AND Date_in IS NOT NULL AND Date_in > Due_date;
            '''
            
            new_returned_fines = [dict(x) for x in c.execute(get_new_returned_fines_query).fetchall()]

            # Fine_amt will be updated with the other existing fines 
            create_new_fine_query = '''
            INSERT INTO FINES (Loan_id, Fine_amt)
            VALUES (:Loan_id, 0);
            '''

            for fine in new_fines:
                c.execute(create_new_fine_query, fine)

            for fine in new_returned_fines:
                c.execute(create_new_fine_query, fine)
            
            # --------------------------------------
            

            # Existing fine, book not returned
            # --------------------------------------
            get_fines_query = "SELECT * FROM BOOK_LOANS NATURAL JOIN FINES WHERE Paid == FALSE AND Date_in IS NULL;"

            fines = [dict(x) for x in c.execute(get_fines_query).fetchall()]

            update_existing_fine_query = '''
            UPDATE FINES
            SET Fine_amt = Cast ((
                JulianDay(CURRENT_DATE) - JulianDay(:Due_date)
            ) As Integer) * 25
            WHERE Loan_id == :Loan_id;
            '''

            for fine in fines:
                c.execute(update_existing_fine_query, fine)


            # Existing fine, book returned
            # --------------------------------------
            get_returned_fines_query = "SELECT * FROM BOOK_LOANS NATURAL JOIN FINES WHERE Paid == FALSE AND Date_in IS NOT NULL;"

            returned_fines = [dict(x) for x in c.execute(get_returned_fines_query).fetchall()]

            update_existing_returned_fine_query = '''
            UPDATE FINES
            SET Fine_amt = Cast ((
                JulianDay(:Date_in) - JulianDay(:Due_date)
            ) As Integer) * 25
            WHERE Loan_id == :Loan_id;
            '''

            for fine in returned_fines:
                c.execute(update_existing_returned_fine_query, fine)


