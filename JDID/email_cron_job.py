#!/usr/bin/python3
"""Cron job to send emails out to accountability partners at deadline"""
from datetime import date
from flask import Flask, render_template
from flask_mail import Mail, Message
from JDID import app
from JDID.classes import storage
import os

print('before app.config shit')

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
    #TODO: change back recipient email to partner email
    all_records = storage.all()
    today = str(date.today())
    print('before going into rec')
    for rec in all_records.values():
        print(rec.goal)
        if str(rec.deadline) == '2018-11-01':
            user_obj = storage.get_user_by_id(rec.user_id)
            subject = "It's time to check up on your friend!"
            sender = os.environ.get('MAIL_USERNAME')
            recipients = 'cheersmelissa@gmail.com'
            cc = user_obj.email
            body = render_template("email_txt_template.html", 
                            user=user_obj, goal=rec)
            html = render_template("email_template.html", user=user_obj, goal=rec)
            msg = Message(subject=subject, sender=sender, recipients=[recipients], cc=[cc], bcc='flyaway0120@gmail.com' body=body, html=html)
            mail.send(msg)
            print("Done: One email sent to " + rec.partner_email)