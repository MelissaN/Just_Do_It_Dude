#!/usr/bin/python3
"""Cron job to send emails out to accountability partners at deadline"""
from JDID import app
from JDID.classes import storage
from datetime import date
from flask import Flask
from flask_mail import Mail, Message
import os


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('MY_EMAIL')
app.config['MAIL_PASSWORD'] = os.environ.get('MY_EMAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


with app.app_context():
    """
       Check daily if today is deadline date for any user's goal
       Email accountability partner and have them confirm if goal accomplished
    """
    today = str(date.today())
    for rec in storage.all().values():
        if (rec.deadline == today):
            msg = Message('Hello from Just Do It Dude!', sender=(
                'MY_EMAIL'), recipients=[rec.partner_email])
            INFORM_GOAL_DEADLINE = "Dear " + rec.accountability_partner + ",/nIt's now the deadline. Has your friend reached their goal to " + rec.goal + "? Please check in with them as they've pledged to " + rec.pledge + "! Click here to confirm: "
            INFORM_GOAL_DEADLINE_HTML = "<p>Dear " + rec.accountability_partner + ",</p><p>It's now the deadline. Has your friend reached their goal to " + rec.goal + "? Please check in with them as they've pledged to " + rec.pledge + "! Click here to confirm: <a href='justdoitdude.com/completion_submit/' + rec.goal_id + "></a></p><p>Love,<p><p>Amy & Melissa from Let's Do It Dude!"
            msg.body = INFORM_GOAL_DEADLINE
            msg.html = INFORM_GOAL_DEADLINE_HTML
            mail.send(msg)
            print("Done: One email sent to " + rec.partner_email)
