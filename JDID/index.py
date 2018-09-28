#!/usr/bin/python3
"""
Module for initiating Flask
"""
from flask import Flask, render_template, url_for, redirect, flash
from forms import GoalForm
app = Flask(__name__)

# security against modifying cookies and CSRF attacks
app.config['SECRET_KEY'] = 'tehe'

goals = [
    {
        'goal': 'Lose 5lbs',
        'date_end': 'October 19, 2018',
        'pledge': '20 buckos',
        'partner': 'JayJay',
        'partner_email': 'lalala@gmail.com'
    }
]


@app.route("/", methods=['GET', 'POST'])
def landing():
    form = GoalForm()
    if form.validate_on_submit():
        # flash sends one-time message
        # flash('Goal successfully created!')
        return redirect(url_for('home'))
    return render_template('landing.html', goals=goals, form=form)


@app.route("/home")
def home():
    return render_template('home.html', title_page='Home')


if __name__ == '__main__':
    app.run(debug=True)
