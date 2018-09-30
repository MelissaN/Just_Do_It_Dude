#!/usr/bin/python3
"""
Module for Flask Forms
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField, BooleanField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from JDID.classes import storage


# python classes that auto convert to HTML forms in template
class GoalForm(FlaskForm):
    """
    Form for creating goals
    """
    goal = StringField('Goal',
                       validators=[DataRequired(), Length(max=100)])
    deadline = DateField('End Date', validators=[
                         DataRequired()], format='%m/%d/%Y')
    pledge = IntegerField('Pledge',
                          validators=[DataRequired()])
    accountability_partner = StringField('Accountability Partner',
                                         validators=[DataRequired(), Length(max=50)])
    partner_email = StringField('Partner Email',
                                validators=[DataRequired(), Email()])
    submit = SubmitField('Wooohoo!')


class RegistrationForm(FlaskForm):
    """
    Form for registering new users
    """
    first_name = StringField('First Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
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
