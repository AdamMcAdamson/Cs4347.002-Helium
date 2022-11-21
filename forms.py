from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, HiddenField
from wtforms.validators import InputRequired, Length, Regexp, Optional



class NewBorrowerForm(FlaskForm):
    cardId = HiddenField()
    ssn = StringField('SSN', validators=[InputRequired(), Length(min=11, max=11,), Regexp('^(?!0{3})(?!6{3})[0-8]\d{2}-(?!0{2})\d{2}-(?!0{4})\d{4}$', message="SSN not in correct format")])
    name = StringField('Name', validators=[InputRequired(), Regexp(r'^[A-Za-z\s\-\']+$', message='Name not valid')])
    phone = StringField('Phone', validators=[Length(max=14), Regexp('^[(][0-9]{3}[)]\s[0-9]{3}[-][0-9]{4}$', message='Phone number not in correct format'), Optional()])
    address = StringField('Address', validators=[InputRequired()])
    submit = SubmitField('Submit') 
