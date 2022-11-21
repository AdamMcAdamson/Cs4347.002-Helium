# store standard routes for web requests
from flask import Blueprint, render_template, flash, redirect
from forms import NewBorrowerForm

views_blueprint = Blueprint('views', __name__)

# create a new borrower 
@views_blueprint.route('/borrow/create', methods=['GET', 'POST'])
def create_borrow():
    form = NewBorrowerForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.name.data}!', 'success') # must have python 3.6 and up 
        # TODO create a page to redirect to after creating a new borrower and validate if ssn is not already in the db
        #return redirect(url_for()) 
    return render_template('new_borrower.html', form=form, title='Create New Borrower')

