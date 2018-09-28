#!/usr/bin/python3
"""Cron job to send emails out to accountability parnters at deadline"""
from app import app
from classes import storage
from datetime import date
from flask import Flask


with app.app_context():
    all_records = storage.all()
#    today = date.today()
#    for rec in all_records.values():
#        try: #start_date is today
#            duration = (rec.deadline - rec.start_date).days
#            #if start_date - date.today() > (duration//4), not editable
#            #if ((rec.start_date - rec.deadline < 5) and ((rec.start_date - today).days) < (duration//4)):
#            print(duration)
#            print(rec.deadline - rec.start_date)
#            if ((rec.deadline - rec.start_date).days > 5):
#                print('more than 5')
#            if (((rec.start_date - today).days) < (duration//4)):
#                print('less than quarter')
#            print("editable")
#        except:
#            pass


#        for rec in all_records.values():
#            goal_obj = rec

    def is_goal_editable(goal_obj):
        today = date.today()
        try:
            duration = (goal_obj.deadline - goal_obj.start_date).days
            editable_period = (duration//4)
            if (duration > 5 and (goal_obj.start_date - today).days < editable_period):
                return True
        except:
            return False

    users_records = storage.all()
    goal_objs_and_editability = list()
    for rec in users_records.values():
        goal_objs_and_editability.append((rec, is_goal_editable(rec)))

    for each in goal_objs_and_editability:
        print(each[0])
        print(each[1])
