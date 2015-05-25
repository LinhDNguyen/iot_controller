#!/usr/bin/env python

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

from project import config


app = Flask(__name__)
if config.DBTYPE == 'sqlite':
    app.config['SQLALCHEMY_DATABASE_URI'] = "%s:///%s" % (config.DBTYPE, config.DBHOST)
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "%s://%s:%s@%s/%s" % (config.DBTYPE, config.DBUSER, config.DBPASS, config.DBHOST, config.DBNAME)
db = SQLAlchemy(app)

# Login manager
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = 'asdkjfoeioa9AKDJ89e3onja;!)4j'

# Create models from tables here
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(80))
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    phone = db.Column(db.String(80))
    note = db.Column(db.String(80))
    password = db.Column(db.String(80))
    is_admin = db.Column(db.Integer, default=0)
    authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, uname='', password='', first_name='', last_name='', email='', phone=None, note=None, is_admin=0):
        self.uname = uname
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.note = note
        self.password = password
        self.is_admin = is_admin

    def __repr__(self):
        return '<User %s - %s>' % (str(self.id), str(self.uname))

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False