"""
models.py

App Engine datastore models

"""


from google.appengine.ext import ndb

class Report(ndb.Model):
	created_at = ndb.DateTimeProperty('c', auto_now=True)
	modified_at = ndb.DateTimeProperty('m', auto_now_add=True)
	google_places_id = ndb.StringProperty('g', required=True)
	crowd_level = ndb.StringProperty('w', required=True)
	comments = ndb.TextProperty('n', required=False)