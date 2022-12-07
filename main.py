from flask import Flask, request, send_file, send_from_directory
from flask_restful import Api
import sqlite3 as sql
import sys

from consts import DB_FILE
from book import Search, Checkout, Checkin
from fines import FinesAll, FinesUpdate, FinesPayment
from borrower import BorrowerCreate

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


# Endpoints
api.add_resource(Search, '/book/search', endpoint='search')

api.add_resource(Checkout, '/book/checkout', endpoint='checkout')

api.add_resource(Checkin, '/book/checkin', endpoint='checkin')

api.add_resource(FinesAll, '/fines/all', endpoint='fines_all')

api.add_resource(FinesUpdate, '/fines/update', endpoint='fines_update')

api.add_resource(FinesPayment, '/fines/payment', endpoint='fines_payment')

api.add_resource(BorrowerCreate, '/borrower/create', endpoint='borrower_create')

if __name__ == '__main__':

    # DB reset command line argument
    for arg in sys.argv:
        if arg == "db-reset":
            with sql.connect(DB_FILE) as conn:
                file = open('./resources/schema.sql', mode = 'r', encoding='utf-8')
                c = conn.cursor()
                c.executescript(file.read())

    app.run(debug=True)
