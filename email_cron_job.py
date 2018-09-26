#!/usr/bin/python3
"""Cron job to send emails out to accountability parnters at deadline"""
from app import app
from classes import storage
from datetime import date
from flask import Flask
from flask_mail import Mail, Message
import os


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('MY_EMAIL')
app.config['MAIL_PASSWORD'] = os.environ.get('MY_EMAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


with app.app_context():
    all_records = storage.all()
    today = str(date.today())
    for rec in all_records.values():
        if (rec.deadline == today):
            msg = Message('Hello from Just Do It Dude!', sender=('MY_EMAIL'), recipients=[rec.partner_email])
            msg.body = "Dear " + rec.accountability_partner + ", It's now the deadline. Has your friend reached their goal to " + rec.goal + "? Please check in with them as they've pledged to " + rec.pledge + "!"
            mail.send(msg)
            print("Done: One email sent to " + rec.partner_email)
