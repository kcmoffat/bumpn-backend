"""
urls.py

URL dispatch route mappings and error handlers

"""
from flask import make_response, jsonify

from application import app
from application import views


## URL dispatch rules
# App Engine warm up handler
# See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

# Create a report
app.add_url_rule('/api/v1/reports/', view_func=views.reports, methods=['POST', 'GET'])

## Error handlers
# Handle 404 errors
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify( { 'error': 'Not found'} ), 404)

@app.errorhandler(400)
def bad_request(error):
	return make_response(jsonify( { 'error': 'Bad request'} ), 400)

@app.errorhandler(401)
def unauthorized(error):
	return make_response(jsonify ( { 'error': 'Unauthorized access'}), 401)