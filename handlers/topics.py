from google.appengine.api import users
from handlers.base import BaseHandler
from models.comment import Comment
from models.topic import Topic
from models.user import User
from utils.decorators import validate_csrf


class TopicAdd(BaseHandler):
    def get(self):
        return self.render_template("topic_add.html")

    @validate_csrf
    def post(self):
        user = users.get_current_user()

        title = self.request.get("title")
        text = self.request.get("text")

        new_topic = Topic.create(title=title, content=text, user=user)

        return self.redirect_to("topic-details", topic_id=new_topic.key.id())

class TopicDetails(BaseHandler):
    def get(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))
        comments = Comment.query(Comment.topic_id == topic.key.id(), Comment.deleted == False).order(Comment.created).fetch()

        params = {"topic": topic, "comments": comments}

        return self.render_template("topic_details.html", params=params)

class EditTopic(BaseHandler):
    @validate_csrf   #I'm evil attacker!!??
    def post(self, topic_id):
        user = users.get_current_user()
        topic = Topic.get_by_id(int(topic_id))

        if topic.author_email == user.email() or users.is_current_user_admin():
            content = self.request.get("content")
            title = self.request.get("title")
            topic.content = content
            topic.title = title
            topic.put()

        return self.redirect_to("topic-details", topic_id=topic.key.id())

class TopicDelete(BaseHandler):
    @validate_csrf
    def post(self, topic_id):
        user = users.get_current_user()
        topic = Topic.get_by_id(int(topic_id))

        if topic.author_email == user.email() or users.is_current_user_admin():
            Topic.delete(topic=topic)

        return self.redirect_to("main-page")

class TopicList(BaseHandler):
    def get(self):
        user = users.get_current_user()
        topics = Topic.query(Topic.deleted == False, Topic.author_email == user.email()).order(-Topic.created).fetch()

        params = {"topics":topics}

        return self.render_template('topic_list.html', params=params)

class UserTopicList(BaseHandler):
    def get(self, user_id):
        u = User.get_by_id(int(user_id))
        topics = Topic.query(Topic.deleted == False, Topic.author_email == u.email).order(-Topic.created).fetch()

        params = {"topics":topics, "u":u}

        return self.render_template("user_topic_list.html", params=params)
