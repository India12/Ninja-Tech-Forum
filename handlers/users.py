from handlers.base import BaseHandler
from google.appengine.api import users
from models.user import User
from models.topic import Topic

class UsersHandler(BaseHandler):
    def get(self):
        params = {}
        user = users.get_current_user()

        if not User.query(User.email == user.email()).fetch():
            contact = User(email=user.email())
            contact.put()
        params["contact_list"] = User.query().fetch()

        return self.render_template("users.html", params=params)
