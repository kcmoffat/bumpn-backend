"""
views.py

URL route handlers

Note that any handler params must match the URL route params.
For example the *say_hello* handler, handling the URL route '/hello/<username>',
  must be passed *username* as the argument.

"""
from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from flask import request, render_template, flash, url_for, redirect, jsonify, abort

from flask_cache import Cache

from application import app
from decorators import login_required, admin_required
from models import Report
from secret_keys import IOS_API_KEY


# Flask-Cache (configured to use App Engine Memcache API)
cache = Cache(app)

def reports():
    if not request.args or not request.args['key'] or request.args['key'] != IOS_API_KEY:
        abort(401)
    if request.method == "POST":
        if not request.json or not 'google_places_id' in request.json or not 'crowd_level' in request.json:
            abort(400)
        if 'comments' in request.json:
            report = Report(
                        google_places_id=request.json['google_places_id'],
                        crowd_level=request.json['crowd_level'],
                        comments=request.json['comments'])
        else:
            report = Report(
                        google_places_id=request.json['google_places_id'],
                        crowd_level=request.json['crowd_level'])
        try:
            report.put()
            "inserted into datastore"
            return jsonify(report.to_dict())
        except CapabilityDisabledError:
            abort(400)
    if len(request.args) == 1:
        reports = Report.query().order(-Report.created_at).fetch(20)
        return jsonify({"reports": [report.to_dict() for report in reports]})
    if len(request.args) > 2:
        abort(400)
    if not request.args['google_places_id']:
        abort(400)
    google_places_id = request.args['google_places_id']
    reports = Report.query(Report.google_places_id==google_places_id).order(-Report.created_at).fetch(20)
    return jsonify({"reports": [report.to_dict() for report in reports]})
