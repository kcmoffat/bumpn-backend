"""
views.py

URL route handlers

Note that any handler params must match the URL route params.
For example the *say_hello* handler, handling the URL route '/hello/<username>',
  must be passed *username* as the argument.

"""

from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError
from flask import request, render_template, flash, url_for, redirect, jsonify, abort
from flask_cache import Cache
from application import app
from models import Report, Search, Request, Call
from secret_keys import IOS_API_KEY
import logging
from google.appengine.api import mail

# OAuth2.0 imports
import httplib2
import os
import sys
import json
from apiclient import discovery
from apiclient.errors import HttpError
from google.appengine.ext.db import Query

from oauth2client.appengine import AppAssertionCredentials

# OAuth2.0 vars
_BUCKET_NAME = 'bumpn-backend-images'
_API_VERSION = 'v1'

# Flask-Cache (configured to use App Engine Memcache API)
cache = Cache(app)

def searches():
    if not request.args or not request.args['key'] or request.args['key'] != IOS_API_KEY:
        abort(401)
    if request.method == "POST":
        if not request.json or not 'google_places_id' in request.json or not 'ios_device_id' in request.json:
            abort(400)
        search = Search(
                    google_places_id = request.json['google_places_id'],
                    ios_device_id=request.json['ios_device_id'])
        if 'name' in request.json:
            search.populate(name=request.json['name'])
        if 'vicinity' in request.json:
            search.populate(vicinity=request.json['vicinity'])
        try:
            search.put()
            return jsonify(search.to_dict())
        except CapabilityDisabledError:
            abort(400)
    elif request.method == "GET":
        if not request.args['ios_device_id']:
            logging.error("request.json: %s", request.json)
            logging.error("request.args[ios_device_id]: %@", request.args['ios_device_id'])
            abort(400)
        ios_device_id = request.args['ios_device_id']
        searches = Search.query(Search.ios_device_id==ios_device_id).order(-Search.created_at).fetch(20)
        searchesDeduped = []
        searchesGooglePlacesIds = set()
        for search in searches:
            if search.google_places_id not in searchesGooglePlacesIds:
                if search.name != None and search.vicinity != None:
                    searchesDeduped.append(search)
                    searchesGooglePlacesIds.add(search.google_places_id)
        logging.info("searchesGooglePlacesIds: %s", searchesGooglePlacesIds)
        return jsonify({"searches": [search.to_dict() for search in searchesDeduped]})
    else:
        abort(401)


def reportsv1():
    if not request.args or not request.args['key'] or request.args['key'] != IOS_API_KEY:
        abort(401)
    if request.method == "POST":
        if not request.json or not 'google_places_id' in request.json or not 'crowd_level' in request.json:
            abort(400)
        report = Report(
                        google_places_id=request.json['google_places_id'],
                        crowd_level=request.json['crowd_level'])
        if 'comments' in request.json:
            report.populate(comments=request.json['comments'])
        if 'ios_device_id' in request.json:
            report.populate(ios_device_id=request.json['ios_device_id'])
        if 'photo_url' in request.json:
            report.populate(photo_url=request.json['photo_url'])
        try:
            # report.put()
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

def reportsv2():
    if not request.args or not request.args['key'] or request.args['key'] != IOS_API_KEY:
        abort(401)
    if request.method == "POST":
        if not request.json or not 'google_places_id' in request.json or not 'tags' in request.json:
            abort(400)
        report = Report(
                        google_places_id=request.json['google_places_id'],
                        tags=request.json['tags'])
        if 'comments' in request.json:
            report.populate(comments=request.json['comments'])
        if 'ios_device_id' in request.json:
            report.populate(ios_device_id=request.json['ios_device_id'])
        if 'photo_url' in request.json:
            report.populate(photo_url=request.json['photo_url'])
        try:
            report.put()
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

def images():
    if not request.args or not request.args['key'] or request.args['key'] != IOS_API_KEY:
        abort(401)
    if not request.args or not request.args['name'] or not request.args['length']:
        logging.error("name: %s", request.args.get('name'))
        logging.error("length: %s", request.args.get('length'))
        abort(401)
    logging.info(request.args)
    name = request.args['name']
    length = request.args['length']
    if request.method == 'GET':
        credentials = AppAssertionCredentials(scope='https://www.googleapis.com/auth/devstorage.read_write')
        http_auth = credentials.authorize(httplib2.Http())
        logging.info("successfully created http_auth object")
    try:
        url = "https://www.googleapis.com/upload/storage/v1/b/" + _BUCKET_NAME + "/o?uploadType=resumable&name=" + name
        resp, content = http_auth.request(url, method="POST", headers={'Content-Length':'0',
                                                 'Content-Type':'application/json; charset=UTF-8',
                                                 'X-Upload-Content-Type':'image/jpeg',
                                                 'X-Upload-Content-Length':length})
        return jsonify(resp)
    except HttpError, e:
        logging.error("response status: %s", e.resp.status)
        logging.error("response content: %s", e.content)

def requestsv2():
    if not request.args or not request.args['key'] or request.args['key'] != IOS_API_KEY:
        abort(401)
    if request.method == "POST":
        if not request.json or not 'google_places_id' in request.json or not 'name' in request.json or not 'vicinity' in request.json:
            abort(400)
        report_request = Request(google_places_id=request.json['google_places_id'],
                                    name=request.json['name'],
                                    vicinity=request.json['vicinity'])
        questions = ''
        more_questions = ''
        if 'ios_device_id' in request.json:
            report_request.populate(ios_device_id=request.json['ios_device_id'])
        if 'questions' in request.json:
            report_request.populate(questions=request.json['questions'])
            questions = request.json['questions']
        if 'more_questions' in request.json:
            report_request.populate(more_questions=request.json['more_questions'])
            more_questions = request.json['more_questions']
        try:
            report_request.put()
            sender_address = "Scout Support <scoutapp14@gmail.com>"
            user_address = "kcmoffat@gmail.com"
            subject = "Update requested at %s" % request.json['name']
            body = """Name: %s\nAddress: %s\nQuestions: %s\nMore Questions: %s""" % (request.json['name'], request.json['vicinity'], ', '.join(questions), more_questions)
            logging.info('questions: %s', ', '.join(questions))
            logging.info('more_questions: %s', more_questions)
            mail.send_mail(sender_address, user_address, subject, body)
            return jsonify(report_request.to_dict())
        except CapabilityDisabledError:
            abort(400)

def callsv2():
    if not request.args or not request.args['key'] or request.args['key'] != IOS_API_KEY:
        abort(401)
    if request.method == "POST":
        if not request.json or not 'google_places_id' in request.json or not 'name' in request.json or not 'vicinity' in request.json:
            abort(400)
        call = Call(google_places_id=request.json['google_places_id'],
                                    name=request.json['name'],
                                    vicinity=request.json['vicinity'])
        if 'ios_device_id' in request.json:
            call.populate(ios_device_id=request.json['ios_device_id'])
        try:
            call.put()
            return jsonify(call.to_dict())
        except CapabilityDisabledError:
            abort(400)