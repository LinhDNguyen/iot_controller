#!/usr/bin/env python

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from project import config


app = Flask(__name__)
if config.DBTYPE == 'sqlite':
    app.config['SQLALCHEMY_DATABASE_URI'] = "%s:///%s" % (config.DBTYPE, config.DBHOST)
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "%s://%s:%s@%s/%s" % (config.DBTYPE, config.DBUSER, config.DBPASS, config.DBHOST, config.DBNAME)
db = SQLAlchemy(app)

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

    def __init__(self, uname='', first_name='', last_name='', email='', phone=None, note=None):
        self.uname = uname
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.note = note

    def __repr__(self):
        return '<User %s - %s>' % (str(self.id), str(self.uname))
