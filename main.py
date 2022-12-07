from flask import Flask, request, send_file, send_from_directory
from flask_restful import Api
import sqlite3 as sql
import sys

from consts import DB_FILE
from book import Search, Checkout, Checkin
from fines import FinesAll, FinesUpdate, FinesPayment

app = Flask(__name__) 
api = Api(app)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

# Serve Static Files
@app.route('/', methods=['GET'])
def index(): 
    return send_file('./public/index.html')

@app.route('/css/<path:path>', methods=['GET'])
def style(path): 
    return send_from_directory('./public/css', path)

@app.route('/scripts/<path:path>', methods=['GET'])
def scripts(path): 
    return send_from_directory('./public/scripts', path)

# @TODO: Move to Own File
@app.route('/borrower/create', methods=['POST'])
def create_borrower():
    
    args = {'ssn':request.args.get('ssn', ''), 'bname':request.args.get('bname', ''), 'address':request.args.get('address', ''), 'phone':request.args.get('phone', 'NULL')}

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
        

# Endpoints
api.add_resource(Search, '/book/search', endpoint='search')

api.add_resource(Checkout, '/book/checkout', endpoint='checkout')

api.add_resource(Checkin, '/book/checkin', endpoint='checkin')

api.add_resource(FinesAll, '/fines/all', endpoint='fines_all')

api.add_resource(FinesUpdate, '/fines/update', endpoint='fines_update')

api.add_resource(FinesPayment, '/fines/payment', endpoint='fines_payment')

if __name__ == '__main__':

    # DB reset command line argument
    for arg in sys.argv:
        if arg == "db-reset":
            with sql.connect(DB_FILE) as conn:
                file = open('./resources/schema.sql', mode = 'r', encoding='utf-8')
                c = conn.cursor()
                c.executescript(file.read())

    app.run(debug=True)
