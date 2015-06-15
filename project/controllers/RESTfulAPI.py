#!/usr/bin/env python

from flask import Flask
from flask import make_response, jsonify
from flask.ext.httpauth import HTTPBasicAuth

from project.models import *
from project import config

auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == config.RESTUID:
        return config.RESTPASS
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

# Lazy view from views module
@auth.login_required
def hello_world():
    return jsonify({'msg': 'Hello world!'})

@auth.login_required
def get_status(ledid):
    res = {
        'id': ledid,
        'status': 'NOT FOUND',
    }

    led = DeviceLed.query.filter_by(id=ledid).first()
    if led:
        res['status'] = led.status

    return jsonify(res)

@auth.login_required
def get_all_status():
    res = []

    leds = DeviceLed.query.all()
    for led in leds:
        res.append({'id': led.id, 'status': led.status})

    return jsonify({'leds':res})
