from handlers.base import BaseHandler
from google.appengine.api import users, memcache
from models.user import User
from models.topic import Topic
from utils.decorators import validate_csrf

class UsersHandler(BaseHandler):
    def get(self):
        params = {}
        user = users.get_current_user()

        if not User.query(User.email == user.email()).fetch():
            contact = User(email=user.email())
            contact.put()
        params["contact_list"] = User.query().fetch()

        return self.render_template("users.html", params=params)

class UserProfileHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        user_profile = User.query(User.email == user.email()).get()

        params = {"user_profile":user_profile}

        return self.render_template("user_profile.html", params=params)

class EditUserProfileHandler(BaseHandler):
    def get(self, user_id):
        user_profile = User.get_by_id(int(user_id))
        params = {"user_profile":user_profile}

        return self.render_template("user_profile.html", params=params)

    @validate_csrf
    def post(self, user_id):
        user_profile = User.get_by_id(int(user_id))
        first_name = self.request.get("first_name")
        last_name = self.request.get("last_name")

        User.edit_profile(user_profile=user_profile, first_name=first_name, last_name=last_name)

        return self.redirect_to("user-profile")

class DeleteUserProfileHandler(BaseHandler):
    def post(self, user_id):
        user = users.get_current_user()
        user_profile = User.get_by_id(int(user_id))

        if user_profile.email == user.email() or users.is_current_user_admin():
            User.delete_profile(user_profile=user_profile)

        return self.redirect_to("main-page")

class LatestTopicsSubscribeHandler(BaseHandler):
    @validate_csrf
    def post(self):
        user = users.get_current_user()
        subscriber = User.query(User.email == user.email()).fetch()[0]

        subscriber.subscribe()

        return self.redirect_to("main-page")

    '''alternative version-subscribe/unsubscribe:

    def post(self, user_id):
        user = users.get_current_user()
        subscriber = User.get_by_id(int(user_id))

        if subscriber.email == user.email():
            User.subscribe(subscriber=subscriber)

        return self.redirect_to("main-page")'''

class LatestTopicsUnsubscribeHandler(BaseHandler):
    @validate_csrf
    def post(self):
        user = users.get_current_user()
        subscriber = User.query(User.email == user.email()).fetch()[0]

        subscriber.unsubscribe()

        return self.redirect_to("main-page")

    '''alternative version-subscribe/unsubscribe:

    def post(self, user_id):
        user = users.get_current_user()
        subscriber = User.get_by_id(int(user_id))

        if subscriber.email == user.email():
            User.unsubscribe(subscriber=subscriber)

        return self.redirect_to("main-page")'''
