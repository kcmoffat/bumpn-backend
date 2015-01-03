"""
models.py

App Engine datastore models

"""


from google.appengine.ext import ndb

class Report(ndb.Model):
	created_at = ndb.DateTimeProperty('c', auto_now=True)
	modified_at = ndb.DateTimeProperty('m', auto_now_add=True)
	google_places_id = ndb.StringProperty('g', required=True)
	crowd_level = ndb.StringProperty('w', required=False)
	comments = ndb.TextProperty('n', required=False)
	ios_device_id = ndb.StringProperty('d', required=False)
	photo_url = ndb.StringProperty('p', required=False)
	tags = ndb.StringProperty('t', repeated=True, required=False)

class Search(ndb.Model):
	created_at = ndb.DateTimeProperty('c', auto_now=True)
	modified_at = ndb.DateTimeProperty('m', auto_now_add=True)
	google_places_id = ndb.StringProperty('g', required=True)
	ios_device_id = ndb.StringProperty('d', required=False)
	name = ndb.StringProperty('n', required=False)
	vicinity = ndb.StringProperty('v', required=False)

class Request(ndb.Model):
	created_at = ndb.DateTimeProperty('c', auto_now=True)
	modified_at = ndb.DateTimeProperty('m', auto_now_add=True)
	google_places_id = ndb.StringProperty('g', required=True)
	ios_device_id = ndb.StringProperty('d', required=False)
	name = ndb.StringProperty('n', required=False)
	vicinity = ndb.StringProperty('v', required=False)
	questions = ndb.StringProperty('q', repeated=True, required=False)
	more_questions = ndb.TextProperty('mq', required=False)

class Call(ndb.Model):
	created_at = ndb.DateTimeProperty('c', auto_now=True)
	modified_at = ndb.DateTimeProperty('m', auto_now_add=True)
	google_places_id = ndb.StringProperty('g', required=True)
	ios_device_id = ndb.StringProperty('d', required=False)
	name = ndb.StringProperty('n', required=False)
	vicinity = ndb.StringProperty('v', required=False)

# class Place(ndb.Model):
# 	created_at = ndb.DateTimeProperty('c', auto_now=True)
# 	modified_at = ndb.DateTimeProperty('m', auto_now_add=True)
# 	google_places_id = ndb.StringProperty('g', required=True)