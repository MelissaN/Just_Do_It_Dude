#!/usr/bin/python3
"""Cron job to send emails out to accountability partners at deadline"""
from datetime import date
from flask import Flask, render_template
from flask_mail import Mail, Message
from JDID.helper_methods import email_goal_confirmation
from JDID import app
from JDID.classes import storage
import os


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


# with app.app_context():
def chron_job():
    """
       Check daily if today is deadline date for any user's goal
       Email accountability partner and have them confirm if goal accomplished
    """
    #TODO: change back recipient email to partner email
    all_records = storage.all()
    today = str(date.today())
    for rec in all_records.values():
        if str(rec.deadline) == today:
            user_obj = storage.get_user_by_id(rec.user_id)
            helper_methods.email_goal_confirmation("It's time to check up on your friend!", os.environ.get('MAIL_USERNAME'), 'flyaway0120@gmail.com',
            render_template("email_txt_template.html", 
                            user=user_obj, goal=rec),
            render_template("email_template.html", 
                            user=user_obj, goal=rec))
            print("Done: One email sent to " + rec.partner_email)
            # msg = Message('Hello from Just Do It Dude!', sender=(
            #     'MY_EMAIL'), recipients=[rec.partner_email])
            # INFORM_GOAL_DEADLINE = "Dear " + rec.accountability_partner + ", It's now the deadline. Has your friend reached their goal to " + rec.goal + "? Please check in with them as they've pledged to " + rec.pledge + "!" + ""
            # msg.body = INFORM_GOAL_DEADLINE
            # mail.send(msg)
