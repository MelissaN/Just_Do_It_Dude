#!/usr/bin/python3
"""Cron job to send emails out to accountability partners at deadline"""
from JDID import app
from datetime import date
from flask import Flask, render_template, url_for
from flask_mail import Mail, Message
from JDID import helper_methods
from JDID.classes import storage
import os


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


with app.app_context(), app.test_request_context(base_url='http://35.221.52.120'):
    """
       Check daily if today is deadline date for any user's goal
       Email accountability partner and have them confirm if goal accomplished
    """
    today = str(date.today())
    for rec in storage.all().values():
        if str(rec.deadline) == today:
            user_obj = storage.get_user_by_id(rec.user_id)
            subject = "It's time to check up on your friend!"
            sender = os.environ.get('MAIL_USERNAME')
            recipients = rec.partner_email
            cc = [user_obj.email]
            helper_methods.email_goal_confirmation(subject, sender, recipients, render_template("email_txt_template.txt", 
                            user=user_obj, goal=rec), render_template("email_template.html", 
                            user=user_obj, goal=rec))
            print("Done: One email sent to " + rec.partner_email)
