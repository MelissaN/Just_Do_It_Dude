#!/usr/bin/python3
"""APP"""
from JDID import app
from flask import abort, jsonify, redirect, request, render_template, flash, url_for
from flask_cors import CORS
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Mail, Message
from JDID import helper_methods
from JDID.forms import GoalForm, RegistrationForm, LoginForm
from JDID.classes import storage
from JDID.classes.models import Goal, User
import os
import random
import requests
import string
from werkzeug.security import check_password_hash


# app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.url_map.strict_slashes = False

cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('MY_EMAIL')
app.config['MAIL_PASSWORD'] = os.environ.get('MY_EMAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route('/', methods=['GET'])
def index():
    """return landing page with goal form"""
    form = GoalForm()
    all_records = storage.all()
    count = storage.count()
    return render_template("landing.html", all_records=all_records.values(), form=form, count=count)


@app.route('/', methods=['POST'])
def display_pledges():
    """return user dashboard summary in response to form submission"""
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
    # helper_methods.email_goal_logged()
    return redirect(url_for("dashboard"))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """return landing page in response to registration"""
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(email=form.email.data,
                        password=form.password.data, first_name=form.first_name.data)

        storage.save(new_user)
        flash('A warm welcome from Melissa and Amy!', 'success')
        login_user(new_user)
        return redirect(url_for('index'))
    return render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """return home page upon login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = storage.get_user_by_email(form.email.data)
        # print(check_password_hash(user.password, form.password.data))
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('display_pledges'))
        else:
            flash("Invalid email or password, buddy", 'danger')
    return render_template("login.html", title="Login", form=form)


@app.route('/logout', methods=['GET'])
#@login_required
def logout():
    """return landing page in response to logout"""
    logout_user()
    flash("See you later. Come back a winner!", "success")
    return redirect(url_for('display_pledges'))


@app.route("/dashboard", methods=['GET'])
@login_required
def dashboard():
    """return user homepage with their goals listed"""
    # TODO: Filter goals so they're specific to logged in user
    users_records = storage.all()
    goal_objs_and_editability = list()
    for rec in users_records.values():
        goal_objs_and_editability.append(
            (rec, helper_methods.is_goal_editable(rec)))
    # print(goal_objs_and_editability)
    return render_template('user_dashboard.html', title_page='Dashboard',
                           goal_objs_and_editability=goal_objs_and_editability)


@app.route("/dashboard", methods=['POST', 'DELETE'])
def update():
    """return user homepage with updated goals listed"""
    # codes for editting goals
    req = request.form
    users_records = storage.all()
    if request.method == 'POST':
        updated_goal = req.get('updated_goal').split(',id=')[0]
        goal_id = req.get('updated_goal').split(',id=')[1]
        for rec in users_records.values():
            if str(rec.id) == goal_id:
                setattr(rec, 'goal', updated_goal)
                storage.save(rec)
                # helper_methods.email_goal_updated()
    else:
        goal_to_delete = req.get('goal_to_delete')
        for rec in users_records.values():
            if str(rec.id) == goal_to_delete:
                msg_goal_deleted = "=( Someone has just forfeited their pledge and will {} to {}".format(
                    rec.pledge, rec.accountability_partner)
                storage.delete(rec)
                # helper_methods.email_goal_deleted()
    return("just updated/deleted")


# @app.errorhandler(404)
# def not_found(error):
    # """return custom 404 page
    #    return render_template("custom_404.html")
    # """
    # pass


@app.after_request
def handle_cors(response):
    """cors"""
    # allow access from other domains
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
