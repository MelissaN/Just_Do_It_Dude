#!/usr/bin/python3
from datetime import datetime, date


def is_goal_editable(goal_obj):
    """return True if goal is longer than 5 days and less than a quarter towards deadline"""
    today = date.today()
    # try:
    duration = (goal_obj.deadline - goal_obj.start_date).days
    editable_period = (duration//4)
    if (duration > 5 and (today - goal_obj.start_date).days < editable_period):
        return True
    else:
        return False
    # except Exception:
    #     return False
    # return False
