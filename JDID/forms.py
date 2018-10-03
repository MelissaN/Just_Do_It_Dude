#!/usr/bin/python3
"""
Module for Flask Forms
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField, BooleanField, DateField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from JDID.classes import storage


# python classes that auto convert to HTML forms in template
class GoalForm(FlaskForm):
    """
    Form for creating goals
    """
    goal = StringField('Goal',
                       validators=[DataRequired(), Length(min=10)])
    deadline = DateField('Deadline', validators=[
                         DataRequired()], format='%m/%d/%Y')
    pledge = StringField('Pledge', validators=[DataRequired(), Length(min=10)])
    accountability_partner = StringField('Accountability Partner',
                                         validators=[DataRequired(), Length(max=50)])
    partner_email = EmailField('Partner Email',
                                validators=[DataRequired(), Email()])
    submit = SubmitField('Set goal!')

#    def validate_partner_email(self, partner_email):
#        # user = storage.get_user_by_email(email.data)
#        if partner_email.data == current_user.email:
#            raise ValidationError('You cannot hold yourself accountable!')
#        return
#

class RegistrationForm(FlaskForm):
    """
    Form for registering new users
    """
    first_name = StringField('First Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = storage.get_user_by_email(email.data)
        if user:
            raise ValidationError('Back off, this email is taken')
        return


class LoginForm(FlaskForm):
    """
    Form for signing in existing users
    """
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
