#!/usr/bin/python3
"""APP"""
from classes import storage
from classes.goal_class import Goal
from flask import abort, Flask, jsonify, redirect, request, render_template
import random
import requests
import string


app = Flask(__name__)
#app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.url_map.strict_slashes = False


@app.errorhandler(404)
def not_found(error):
    """return custom 404 page
       return render_template("custom_404.html")
    """
    pass


@app.route('/', methods=['GET'])
def index():
    """return landing page with goal form"""
    all_pledges = storage.all()
    return render_template("index.html", all_pledges=all_pledges.values())


@app.route('/', methods=['POST'])
def display_pledges():
    """return summary in response to form submission"""
    goal = request.form["goal"]
    deadline = request.form["deadline"]
    pledge = request.form["pledge"]
    friends_email = request.form["friends_email"]
    username = request.form["username"]
    attributes = {"goal": goal, "deadline": deadline, "pledge": pledge,
                  "friends_email": friends_email, "username": username}
    obj = Goal(**attributes)
    storage.save(obj)
    all_pledges = storage.all()
    return render_template("index.html", all_pledges=all_pledges.values())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
