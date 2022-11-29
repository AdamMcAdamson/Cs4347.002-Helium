from flask import Flask, request, jsonify, render_template, flash, redirect, send_file, send_from_directory
from flask_restful import Resource, Api
from forms import NewBorrowerForm
from views import views_blueprint
import sqlite3 as sql
import sys

from consts import DB_FILE
from book import Search, Checkout, Checkin
from fines import FinesAll, FinesUpdate

app = Flask(__name__) 
api = Api(app)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

# Register the blueprints 
app.register_blueprint(views_blueprint, url_prefix='/views')

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

# @TODO: Remove
class Quote(Resource):
    def get(self):
        args = request.args
        with sql.connect(DB_FILE) as conn:
            conn.row_factory = sql.Row
            c = conn.cursor()
            #return jsonify({"message": 200, "success":True, "data": [dict(x) for x in (c.execute('SELECT * FROM quote').fetchall())]})
            return [dict(x) for x in (c.execute('SELECT * FROM quote').fetchall())]

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
        return {"message": "Borrower Successfully Created. Card ID: " + card_id + ".", "card_id": card_id}, 200
        

# Endpoints
api.add_resource(Search, '/book/search', endpoint='search')

api.add_resource(Checkout, '/book/checkout', endpoint='checkout')

api.add_resource(Checkin, '/book/checkin', endpoint='checkin')

api.add_resource(FinesAll, '/fines/all', endpoint='fines_all')

api.add_resource(FinesUpdate, '/fines/update', endpoint='fines_update')

# @TODO: Remove
api.add_resource(Quote, '/quote', endpoint='quote')

if __name__ == '__main__':

    # DB reset command line argument
    for arg in sys.argv:
        if arg == "db-reset":
            with sql.connect(DB_FILE) as conn:
                file = open('./resources/schema.sql', mode = 'r', encoding='utf-8')
                c = conn.cursor()
                c.executescript(file.read())

    app.run(debug=True)
