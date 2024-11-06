from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from database import *

class RegistrationForm(FlaskForm):
    name = StringField('Name',
                             validators=[DataRequired()])
    surname = StringField('Surname',
                             validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(),Email()])
    phonenum = StringField('Phone')
    address = StringField('Address',
                             validators=[DataRequired()])
    password = PasswordField('password',
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                             validators=[DataRequired(),EqualTo('password')])
    type = SelectField('Account type',
                       choices=[('Seller'), ('Customer')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(),Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    submit = SubmitField('Log In')