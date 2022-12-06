import sqlite3 as sql
from flask import request
from flask_restful import Resource

from consts import DB_FILE#, SEARCH_PAGE_SIZE

class FinesPayment(Resource):

    def put(self):

        args = {'loan_id':request.args.get('loan_id', '')}

        # @TODO: Fix
        with sql.connect(DB_FILE) as conn:
            conn.row_factory = sql.Row
            c = conn.cursor()

            verify_returned_query = '''
            SELECT COUNT(*) AS count
            FROM BOOK_LOANS
            WHERE Loan_id = :loan_id AND Date_in IS NOT NULL;
            '''
            
            if dict(c.execute(verify_returned_query, args).fetchone())['count'] != 1:
                return {"message" : "Cannot pay fine. The book has not been returned."}, 409
            
            check_fine_query = '''
            SELECT COUNT(*) AS count
            FROM FINES
            WHERE Loan_id == :loan_id AND Paid == 0;
            '''

            if dict(c.execute(check_fine_query, args).fetchone())['count'] != 1:
                return {"message" : "Cannot pay fine. The request fine has either already been paid, or does not exist."}, 409

            pay_fine_query = '''
            UPDATE FINES
            SET Paid = 1
            WHERE Loan_id == :loan_id;
            '''

            c.execute(pay_fine_query, args)

            return {"message": "Paid fine successfully."} , 200

class FinesAll(Resource):

    # @TODO: Pagination or no?
    def get(self):

        args = {'paid':request.args.get('paid', '')}

        with sql.connect(DB_FILE) as conn:
            conn.row_factory = sql.Row
            c = conn.cursor()
            if args['paid'] == '':
                sql_query = '''SELECT *
                FROM FINES NATURAL JOIN BOOK_LOANS
                ORDER BY Card_id;'''
            else: 
                sql_query = '''SELECT *
                FROM FINES NATURAL JOIN BOOK_LOANS
                WHERE Paid == FALSE
                ORDER BY Card_id;'''

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
            SELECT BOOK_LOANS.Loan_id As Loan_id
            FROM (BOOK_LOANS LEFT JOIN FINES ON BOOK_LOANS.Loan_id = FINES.Loan_id)
            WHERE Paid IS NULL AND Date_in IS NULL AND DATE(CURRENT_DATE) > Due_date;
            '''

            new_fines = [dict(x) for x in c.execute(get_new_fines_query).fetchall()]

            # book returned
            get_new_returned_fines_query = '''
            SELECT BOOK_LOANS.Loan_id As Loan_id
            FROM (BOOK_LOANS LEFT JOIN FINES ON BOOK_LOANS.Loan_id = FINES.Loan_id)
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

            return {"message": "success"}, 200


