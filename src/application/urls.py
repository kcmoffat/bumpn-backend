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
app.add_url_rule('/api/v1/reports/', view_func=views.reportsv1, methods=['POST', 'GET'])
app.add_url_rule('/api/v2/reports/', view_func=views.reportsv2, methods=['POST', 'GET'])

# Create a search log
app.add_url_rule('/api/v1/searches/', view_func=views.searches, methods=['POST'])
app.add_url_rule('/api/v2/searches/', view_func=views.searches, methods=['POST', 'GET'])

# Upload an image (return an uploadID for direct upload to Google Cloud Storage)
app.add_url_rule('/api/v1/images/', view_func=views.images, methods=['GET'])
app.add_url_rule('/api/v2/images/', view_func=views.images, methods=['GET'])

# Create a report request
app.add_url_rule('/api/v2/requests/', view_func=views.requestsv2, methods=['POST'])

# Create a call log
app.add_url_rule('/api/v2/calls/', view_func=views.callsv2, methods=['POST'])

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