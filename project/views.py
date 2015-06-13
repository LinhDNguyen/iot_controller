#!/usr/bin/env python
import bcrypt
from flask import Flask
from flask import request
from flask import render_template
from flask import session
from flask import url_for
from flask import redirect
from flask import jsonify
from flask.ext.login import login_required
from flask.ext.login import login_user
from flask.ext.login import logout_user
from flask.ext.login import current_user

from project import config
from project.models import *
from project.forms import *
from project.controllers import hello

@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve
    """
    return User.query.filter_by(id=user_id).first()

# All views below
@app.route("/")
@login_required
def index():
    users = User.query.all()
    if ('user_id' in session.keys()) and (not session['user_id']):
        session.current_user = None
    else:
        session.current_user = current_user
    return render_template('index.html',
                            session = session,
                            users = users,)

@app.route("/control")
@login_required
def control():

    if ('user_id' in session.keys()) and (not session['user_id']):
        session.current_user = None
    else:
        session.current_user = current_user
    return render_template('control.html',
                            session = session,)

@app.route("/manager")
@login_required
def manager():

    if ('user_id' in session.keys()) and (not session['user_id']):
        session.current_user = None
    else:
        session.current_user = current_user
    return render_template('manager.html',
                            session = session,)

@app.route("/profile")
@login_required
def profile():

    if ('user_id' in session.keys()) and (not session['user_id']):
        session.current_user = None
    else:
        session.current_user = current_user
    return render_template('profile.html',
                            session = session,)

# Error Pages
@app.errorhandler(500)
def error_page(e):
    return render_template('error_pages/500.html'), 500

@app.errorhandler(404)
def not_found(e):
    return render_template('error_pages/404.html'), 404

@app.route("/login", methods=["GET", "POST"])
def login():
    """For GET requests, display the login form. For POSTS, login the current user
    by processing the form."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(uname=form.uname.data).first()
        if user:
            if bcrypt.hashpw(str(form.password.data.encode('utf-8')), user.password.encode('utf-8')) == user.password:
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                session.current_user = current_user
                return redirect(url_for("index"))
    return render_template("login.html", form=form)

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    session.current_user = None
    return redirect(url_for("login"))

@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    return redirect(url_for("login"))

@app.route("/rest/get_status/<int:ledid>", methods=["GET"])
def get_status(ledid):
    res = {
        'id': ledid,
        'status': 'NOT FOUND',
    }

    led = DeviceLed.query.filter_by(id=ledid).first()
    if led:
        res['status'] = led.status

    return jsonify(res)

# Lazy Views
app.add_url_rule('/hello', view_func=hello.hello_world)



