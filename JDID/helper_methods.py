#!/usr/bin/python3
"""
   HELPER METHODS
      logged_in:           returns True if user is logged in
      is_goal_editable:    returns True is goal is still within editing period
      progress_percentage: return percentage of time along the way to deadline
      email_goal_logged:   emails accountability partner friend's new goal
      email_goal_updated:  emails accountability partner friend's updated goal
      email_goal_deleted:  emails accountability partner friend's deleted goal
"""
from datetime import datetime, date
from flask import Flask
from flask_mail import Message, Mail
from JDID import app
import os
from threading import Thread


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


def logged_in(current_user):
    """returns True if user is logged in"""
    try:
        _ = current_user.id
        return True
    except:
        return False


def is_goal_editable(goal_obj):
    """return True if goal is longer than 5 days and less than a quarter towards deadline"""
    today = date.today()
    # print("goal:", goal_obj.goal, " start: ", goal_obj.start_date, " deadline: ", goal_obj.deadline, " duration: ", (goal_obj.deadline - goal_obj.start_date).days, " edit pd: ", (goal_obj.deadline - goal_obj.start_date).days//4)
    try:
        duration = (goal_obj.deadline - goal_obj.start_date).days
        editable_period = (duration//4)
        if (duration > 5 and (today - goal_obj.start_date).days < editable_period):
            return True
    except:
        return False
    return False


def days_passed(goal_obj):
    """return number of days passed since goal creation"""
    # print("goal: ", goal_obj.goal, " start: ", goal_obj.start_date, " deadline: ", goal_obj.deadline, " duration: ", (goal_obj.deadline - goal_obj.start_date).days, " edit pd: ", (goal_obj.deadline - goal_obj.start_date).days//4, " days passed: ", (date.today() - goal_obj.start_date).days)
    # print("days_passed/duration = ", ((((date.today() - goal_obj.start_date).days) / (goal_obj.deadline - goal_obj.start_date).days) * 100))
    return ((date.today() - goal_obj.start_date).days)


def progress_percentage(goal_obj):
    """return percentage of time along the way to deadline"""
    s = str((((date.today() - goal_obj.start_date).days) / (goal_obj.deadline - goal_obj.start_date).days) * 100)
    return (int(s.split(".")[0]))


def email_goal_logged(user, goal):
    """emails accountability partner friend's new goal"""
    msg = Message('Hello from Just Do It Dude!', sender=(
        os.environ.get('MAIL_USERNAME')), recipients=[goal.partner_email], cc=[user.email])
    INFORM_GOAL_LOGGED = "Dear " + goal.accountability_partner + ",\n\nWoohoo! Starting now, " + user.first_name + " has a goal to " + goal.goal + " by " + str(goal.deadline) + ". Even cooler, they've asked that you hold them accountable. If they don't succeed in accomplishing their goal by their deadline, in their own words they've pledged to '" + goal.pledge + "!'\n\nWe'll email you again on their deadline to ask you to confirm if they've succeeded!\n\nLove,\nAmy and Melissa from Just Do It Dude!"
    msg.body = INFORM_GOAL_LOGGED
    with app.app_context():
        print("emailing at goal creation in app_context")
        mail.send(msg)
    print("emailed at goal creation")


def email_goal_updated(goal):
    """emails accountability partner friend's updated goal"""
    msg = Message('Your friend updated their goal!', sender=(
        os.environ.get('MAIL_USERNAME')), recipients=[goal.partner_email])
    INFORM_GOAL_UPDATED = "Hello again " + goal.accountability_partner + ",\n\nWe thought you'd like to know that one of your friends has modified their goal. Now, they plan to " + goal.goal + " by " + str(goal.deadline) + ". Remember that they've asked that you hold them accountable. If they don't succeed in accomplishing their goal by their deadline, in their own words they've pledged to '" + goal.pledge + "!'\n\nWe'll email you again on their deadline to ask you to confirm if they've succeeded!\nLove,\nAmy and Melissa from Just Do It Dude!"
    msg.body = INFORM_GOAL_UPDATED
    with app.app_context():
        mail.send(msg)


def email_goal_deleted(goal):
    """emails accountability partner friend's deleted goal"""
    msg = Message('Your friend forfeited their pledge!', sender=(
        os.environ.get('MAIL_USERNAME')), recipients=[goal.partner_email])
    INFORM_GOAL_DELETED = "Dear " + goal.accountability_partner + ",\n\nThis is to notify you that one of your friends unfortunately dropped their goal to " + goal.goal + " by " + str(goal.deadline) + ". In doing so, they've forfeited their pledge. Since they've asked that you hold them accountable, they've promised you this: " + goal.pledge + ". Do check in with them!\n\nLove,\nAmy and Melissa from Just Do It Dude!"    
    msg.body = INFORM_GOAL_DELETED
    with app.app_context():
        mail.send(msg)
