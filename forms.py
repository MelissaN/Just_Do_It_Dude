#!/usr/bin/python3
"""
Module for Flask Forms
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField, BooleanField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo


# python classes that auto convert to HTML forms in template
class GoalForm(FlaskForm):
    goal = StringField('Goal',
                       validators=[DataRequired(), Length(max=100)])
    deadline = DateField('End Date', validators=[DataRequired()])
    pledge = IntegerField('Pledge',
                          validators=[DataRequired()])
    accountability_partner = StringField('Accountability Partner',
                          validators=[DataRequired(), Length(max=50)])
    partner_email = StringField('Partner Email',
                                validators=[DataRequired(), Email()])
    submit = SubmitField('Wooohoo!')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=4, max=20)])
    password = StringField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
