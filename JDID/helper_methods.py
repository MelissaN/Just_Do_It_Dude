#!/usr/bin/python3
"""
   HELPER METHODS
      is_goal_editable:   returns True is goal is still within editing period
      email_goal_logged:  emails accountability partner friend's new goal
      email_goal_updated: emails accountability partner friend's updated goal
      email_goal_deleted: emails accountability partner friend's deleted goal

"""
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


def email_goal_logged():
    """emails accountability partner friend's new goal"""
    msg = Message('Hello from Just Do It Dude!', sender=(
        os.environ.get('MY_EMAIL')), recipients=[partner_email])
    INFORM_GOAL_LOGGED = "Dear " + accountability_partner + ",\nWoohoo! Starting now, one of your friends has a goal to " + goal + " by " + deadline + ". Even cooler, they've asked that you hold them accountable. If they don't succeed in accomplishing their goal by their deadline, in their own words they've pledged to '" + pledge + "!'\nWe'll email you again on their deadline to ask you to confirm if they've succeeded!\nLove,\nAmy and Melissa from Just Do It Dude!"
    msg.body = INFORM_GOAL_LOGGED
    mail.send(msg)


def email_goal_updated():
    """emails accountability partner friend's updated goal"""
    msg = Message('Hello from Just Do It Dude!', sender=(
        os.environ.get('MY_EMAIL')), recipients=[partner_email])
    INFORM_GOAL_UPDATED = "Hello again " + accountability_partner + ",\nWe thought you'd like to know that one of your friends modified their goal. Now, they plan to " + goal + " by " + deadline + ". Remember that they've asked that you hold them accountable. If they don't succeed in accomplishing their goal by their deadline, in their own words they've pledged to '" + pledge + "!'\nWe'll email you again on their deadline to ask you to confirm if they've succeeded!\nLove,\nAmy and Melissa from Just Do It Dude!"
    msg.body = INFORM_GOAL_UPDATED
    mail.send(msg)


def email_goal_deleted():
    """emails accountability partner friend's deleted goal"""
    msg = Message('Hello from Just Do It Dude!', sender=(
        os.environ.get('MY_EMAIL')), recipients=[partner_email])
    INFORM_GOAL_DELETED = "Dear " + accountability_partner + ",\nThis is to notify you that your friend has unfortunately dropped their goal to " + goal + " by " + deadline + ". In doing so, they've forfeited their pledge. Since they've asked that you hold them accountable, they've promised you this: " + pledge + ". Do check in with them!\nLove,\nAmy and Melissa from Just Do It Dude!"    
    msg.body = INFORM_GOAL_DELETED
    mail.send(msg)
