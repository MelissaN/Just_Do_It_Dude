#!/usr/bin/python3
"""APP"""
from flask import abort, jsonify, redirect, request, render_template, flash, url_for, make_response, session
from flask_cors import CORS
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Mail, Message
import hashlib
from JDID import app
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


@app.route('/', methods=['GET'])
def index():
    """show feed of goals and pledges"""
    uin = helper_methods.logged_in(current_user)
    form = GoalForm()
    count = storage.count()
    goals_and_days_passed = list()
    for rec in storage.all().values():
        goals_and_days_passed.append((rec, helper_methods.days_passed(rec)))
    return render_template("landing.html", uin=uin, form=form, count=count, goals_and_days_passed=goals_and_days_passed)


@app.route('/create_goal', methods=['POST'])
def create_goal():
    """POST goal to database if logged in
        else save goal obj in cookie and update it's user_id once logged in
    """
    form = GoalForm()
    if form.validate_on_submit():
        obj = Goal(goal=form.goal.data, deadline=form.deadline.data,
                   accountability_partner=form.accountability_partner.data,
                   partner_email=form.partner_email.data, pledge=form.pledge.data)
        storage.save(obj)
        if current_user.is_authenticated:
            setattr(obj, 'user_id', current_user.id)
            storage.save(obj)
            flash('Successfully made a commitment!', 'success')
            helper_methods.email_goal_logged(current_user, obj)
            return redirect(url_for('dashboard'))
        else:
            session['cookie'] = obj.id
            flash("Please login first!")
            return redirect(url_for("login"))
    return redirect(url_for("dashboard"))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """return landing page in response to registration"""
    uin = helper_methods.logged_in(current_user)
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(email=form.email.data,
                        password=form.password.data, first_name=form.first_name.data)

        storage.save(new_user)
        flash('A warm welcome from Melissa and Amy!', 'success')
        login_user(new_user)
        return redirect(url_for('dashboard'))
    return render_template("register.html", uin=uin, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """return home page upon login"""
    uin = helper_methods.logged_in(current_user)
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = storage.get_user_by_email(form.email.data)
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password, buddy", 'danger')
    return render_template("login.html", uin=uin, title="Login", form=form)


@app.route('/logout', methods=['GET'])
def logout():
    """return landing page in response to logout"""
    logout_user()
    flash("See you later. Come back a winner!", "success")
    return redirect(url_for('dashboard'))


@app.route("/dashboard", methods=['GET'])
@login_required
def dashboard():
    """return user homepage with their goals listed"""
    uin = helper_methods.logged_in(current_user)
    try:
        if session['cookie']:
            goal_id = session['cookie']
            goal_obj = storage.get_goal_by_id(goal_id)
            setattr(goal_obj, 'user_id', current_user.id)
            storage.save(goal_obj)
            session['cookie'] = None
            helper_methods.email_goal_logged(current_user, goal_obj)
    except KeyError:
        pass
    user = storage.get_user_by_id(current_user.id)
    goal_objs_and_editability = list()
    for rec in user.goals:
        goal_objs_and_editability.append(
            (rec, helper_methods.is_goal_editable(rec),
             helper_methods.days_passed(rec), helper_methods.progress_percentage(rec)))
    return render_template('user_dashboard.html', uin=uin, user=user, title_page='Dashboard',
                           goal_objs_and_editability=goal_objs_and_editability)


@app.route("/dashboard", methods=['POST', 'DELETE'])
def update():
    """return user homepage with updated goals listed"""
    # codes for editting goals
    req = request.form
    if request.method == 'POST':
        updated_line = req.get('updated_goal').split('</span>')[1]
        updated_goal = updated_line.split(',id=')[0]
        goal_id = updated_line.split(',id=')[1]
        for rec in storage.all().values():
            if str(rec.id) == goal_id:
                setattr(rec, 'goal', updated_goal)
                storage.save(rec)
                helper_methods.email_goal_updated(rec)
    else:
        goal_to_delete = req.get('goal_to_delete')
        for rec in storage.all().values():
            if str(rec.id) == goal_to_delete:
                helper_methods.email_goal_deleted(rec)
                storage.delete(rec)
    return("just updated/deleted")


@app.route("/completion/<goal_id>", methods=['GET'])
def confirm_completion(goal_id):
    """return page for accountability partner to confirm yes or no"""
    goal_obj = storage.get_goal_by_id(goal_id)
    user = storage.get_user_by_id(goal_obj.user_id)
    return render_template("completion.html", user=user, goal=goal_obj)


@app.route("/completion_update/<goal_id>", methods=['GET'])
def completion_submit(goal_id):
    """store the completion status in database's goal object"""
    is_completed = request.args.get('complete', None)
    goal_obj = storage.get_goal_by_id(goal_id)
    if goal_obj:
        setattr(goal_obj, 'completed', bool(is_completed))
        storage.save(goal_obj)
    flash("You've successfully evaluated your friend's goal", 'success')
    return redirect(url_for("index"))


@app.errorhandler(404)
def not_found(error):
    """return custom 404 page
       return render_template("custom_404.html")
    """
    return ({error: "Page Not Found"}, 404)



@app.after_request
def handle_cors(response):
    """cors"""
    # allow access from other domains
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
