#!/usr/bin/python3
"""Cron job to send emails out to accountability partners at deadline"""
from datetime import date
from flask import Flask, render_template
from flask_mail import Mail, Message
#from JDID import app
from JDID.classes import storage
import os

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


with app.app_context():
    """
       Check daily if today is deadline date for any user's goal
       Email accountability partner and have them confirm if goal accomplished
    """
with app.app_context():
    """
       Check daily if today is deadline date for any user's goal
       Email accountability partner and have them confirm if goal accomplished
    """
    #TODO: change back recipient email to partner email after testing
    today = str(date.today())
    for rec in storage.all().values():
        if str(rec.deadline) == "2018-10-06":
            print("found deadline")
            user_obj = storage.get_user_by_id(rec.user_id)
            subject = "It's time to check up on your friend!"
            sender = os.environ.get('MAIL_USERNAME')
            recipients = os.environ.get('MAIL_USERNAME')
            print("sender: ", sender, " recipients: ", recipients)
            cc = [user_obj.email, "flyaway0120@gmail.com"]
            body = render_template("email_txt_template.html", user=user_obj, goal=rec)
            html = render_template("email_template.html", user=user_obj, goal=rec)
            msg = Message(subject=subject, sender=sender, recipients=[recipients], cc=[cc], body=body, html=html)
            print("Trying to send to " + rec.partner_email)
            mail.send(msg)
            print("Done: One email sent to " + rec.partner_email)
