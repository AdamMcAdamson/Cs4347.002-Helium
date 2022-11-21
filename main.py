from flask import Flask, request, jsonify, render_template, flash, redirect
from flask_restful import Resource, Api
from forms import NewBorrowerForm
from views import views_blueprint
import sqlite3 as sql

from consts import DB_FILE
from search import Search

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
# Register the blueprints 
app.register_blueprint(views_blueprint, url_prefix='/views')

def index(): 
    return app.send_static_file('index.html')

app.add_url_rule('/', 'index', index)


"""
def create_borrower():
    
    args = request.args

    ssn = args.get("ssn")
    bname = args.get("bname")
    address = args.get("address")
    phone = args.get("phone", "NULL")

    # @TODO: Check for NULL values and return error if so
    # @TODO: Sanitize ssn and phone number into proper form:
    #   ssn - 123-456-7890
    #   phone - (555) 555-5555
    with sql.connect('HeliumDB.db') as conn:
        conn.row_factory = sql.Row
        c = conn.cursor()
        # Check for existing SSN and return useful error if it already exists
        if c.execute('SELECT * FROM BORROWER WHERE Ssn = ?', (ssn,)).fetchone():
            return "Only one borrower card per person. Ssn must be unique.",409
        # Create borrower
        command = "INSERT INTO BORROWER (Ssn, Bname, Address, Phone) VALUES (?, ?, ?, ?);"
        c.execute(
            command,
            (ssn, bname, address, phone,)
        )
        return "Success",200
"""
@app.route('/borrower/create', methods=['GET', 'POST'])
def create_borrower():
    form = NewBorrowerForm()
    #args = request.args
    if form.validate_on_submit():
        ssn = request.form["ssn"]
        bname = request.form["name"]
        address = request.form["address"]
        phone = request.form["phone"]

        # @TODO: Check for NULL values and return error if so
        # @TODO: Sanitize ssn and phone number into proper form:
        #   ssn - 123-456-7890
        #   phone - (555) 555-5555
        with sql.connect('HeliumDB.db') as conn:
            conn.row_factory = sql.Row
            c = conn.cursor()
            # Check for existing SSN and return useful error if it already exists
            if c.execute('SELECT * FROM BORROWER WHERE Ssn = ?', (ssn,)).fetchone():
                flash(f'Only one borrower card per person. Ssn must be unique.', 'danger')
                return render_template('new_borrower.html', form=form, title='Create New Borrower')
                #return "Only one borrower card per person. Ssn must be unique.",409
            # Create borrower
            command = "INSERT INTO BORROWER (Ssn, Bname, Address, Phone) VALUES (?, ?, ?, ?);"
            c.execute(
                command,
                (ssn, bname, address, phone,)
            )
            flash(f'Account created for {form.name.data}!', 'success')
            # TODO add redirection page
    return render_template('new_borrower.html', form=form, title='Create New Borrower')



api.add_resource(Quote, '/quote', endpoint='quote')




#app.add_url_rule('/borrower/create', 'create_borrower', create_borrower, methods=["POST"])


api.add_resource(Search, '/book/search', endpoint='search')


if __name__ == '__main__':

    with sql.connect(DB_FILE) as conn:
        file = open('./resources/schema.sql', mode = 'r', encoding='utf-8')
        c = conn.cursor()
        c.executescript(file.read())

    app.run(debug=True)
