#!/usr/bin/python3
"""APP"""
from classes import storage
from classes.goal_class import Goal
from flask import abort, Flask, jsonify, redirect, request, render_template, flash
from forms import GoalForm
import random
import requests
import string


app = Flask(__name__)
#app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.url_map.strict_slashes = False

# security against modifying cookies and CSRF attacks
app.config['SECRET_KEY'] = 'tehe'


@app.errorhandler(404)
def not_found(error):
    """return custom 404 page
       return render_template("custom_404.html")
    """
    pass


@app.route('/', methods=['GET'])
def index():
    """return landing page with goal form"""
    form = GoalForm()
    all_records = storage.all()
    return render_template("landing.html", all_records=all_records.values(), form=form)


@app.route('/', methods=['POST'])
def display_pledges():
    """return summary in response to form submission"""
    goal = request.form["goal"]
    deadline = request.form["deadline"]
    accountability_partner = request.form["accountability_partner"]
    partner_email = request.form["partner_email"]
    pledge = request.form["pledge"]
    attributes = {"goal": goal, "deadline": deadline,
                  "accountability_partner": accountability_partner,
                  "partner_email": partner_email, "pledge": pledge}
    obj = Goal(**attributes)
    storage.save(obj)
    all_records = storage.all()
    return render_template("landing.html", all_records=all_records.values())


@app.route("/home")
def home():
    return render_template('home.html', title_page='Home')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
