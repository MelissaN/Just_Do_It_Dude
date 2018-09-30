#!/usr/bin/python3
from datetime import datetime, date


def is_goal_editable(goal_obj):
    """return True if goal is longer than 5 days and less than a quarter towards deadline"""
    today = date.today()
    try:
        duration = (goal_obj.deadline - goal_obj.start_date).days
        editable_period = (duration//4)
        if (duration > 5 and (today - goal_obj.start_date).days < editable_period):
            return True
    except:
        return False
    return False


def email_accountability_partner():
    """send email to accountability partner to inform them of new goal submission"""
    msg = Message('Hello from Just Do It Dude!', sender=(
        os.environ.get('MY_EMAIL')), recipients=[partner_email])
    msg.body = "Dear " + accountability_partner + ", Woohoo! Starting now, your friend has a goal to " + goal + " by " + deadline + ". Even cooler, they've asked that you hold them accountable. If they don't succeed in accomplishing their goal by their deadline, in their own words they've pledged to '" + pledge + "!'"
    mail.send(msg)
