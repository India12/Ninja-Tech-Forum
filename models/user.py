from google.appengine.ext import ndb

class User(ndb.Model):
	first_name = ndb.StringProperty()
	last_name = ndb.StringProperty()
	email = ndb.StringProperty()
	admin = ndb.BooleanProperty(default=False)
	is_subscribed = ndb.BooleanProperty(default=False)
	created = ndb.DateTimeProperty(auto_now_add=True)
	updated = ndb.DateTimeProperty(auto_now=True)
	deleted = ndb.BooleanProperty(default=False)

	def subscribe(self):
		self.is_subscribed = True
		self.put()

	def unsubscribe(self):
		self.is_subscribed = False
		self.put()

	'''alternative version-subscribe/unsubscribe:

	@classmethod
	def subscribe(cls, subscriber):
		subscriber.is_subscribed = True
		subscriber.put()

		return subscriber

	@classmethod
	def unsubscribe(cls, subscriber):
		subscriber.is_subscribed = False
		subscriber.put()

		return subscriber'''

	@classmethod
	def create(cls, email):
		users = cls.query(cls.email == email).fetch()
		if len(users) == 0:
			user = cls(email=email)
			user.put()
			return user

		return False

	@classmethod
	def edit_profile(cls, user_profile, first_name, last_name):
		user_profile.first_name = first_name
		user_profile.last_name = last_name
		user_profile.put()

		return user_profile

	@classmethod
	def delete_profile(cls, user_profile):
		user_profile.deleted = True
		user_profile.key.delete()
