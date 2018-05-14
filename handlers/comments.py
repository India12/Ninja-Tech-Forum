from handlers.base import BaseHandler
from google.appengine.api import users
from models.comment import Comment
from models.topic import Topic
from utils.decorators import validate_csrf
from google.appengine.ext import ndb
from handlers.topics import Topic
from models.user import User


class CommentAdd(BaseHandler):
    @validate_csrf
    def post(self, topic_id):
        user = users.get_current_user()

        if not user:
            return self.write("Please login before posting a comment.")

        text = self.request.get("comment-text")
        topic = Topic.get_by_id(int(topic_id))

        Comment.create(content=text, user=user, topic=topic)

        return self.redirect_to("topic-details", topic_id=topic.key.id())

class EditComment(BaseHandler):
    #@validate_csrf
    def post(self, comment_id):
        user = users.get_current_user()
        comment = Comment.get_by_id(int(comment_id))

        if comment.author_email == user.email() or users.is_current_user_admin():
            content = self.request.get("content")
            comment.content = content
            comment.put()

        return self.redirect_to("topic-details", topic_id=comment.topic_id)

class CommentDelete(BaseHandler):
    @validate_csrf
    def post(self, comment_id):
        comment = Comment.get_by_id(int(comment_id))

        user = users.get_current_user()

        if comment.author_email == user.email() or users.is_current_user_admin():
            Comment.delete(comment=comment)

        return self.redirect_to("topic-details", topic_id=comment.topic_id)

class CommentsList(BaseHandler):
    def get(self):
        user = users.get_current_user()
        topics = Topic.query(Topic.deleted == False).fetch()
        comments = Comment.query(Comment.author_email == user.email(), Comment.deleted == False).order(-Comment.created).fetch()
        topics_titles = ""
        for topic in topics:
            if topic.title == Comment.topic_title:
                topics_titles = set(comment.topic_title for comment in comments)

        params = {'comments': comments,'topics_titles': topics_titles, "topics":topics}

        return self.render_template('comments_list.html', params=params)

class UserCommentsList(BaseHandler):
    def get(self, user_id):
        u = User.get_by_id(int(user_id))
        comments = Comment.query(Comment.deleted == False, Comment.author_email == u.email).order(-Comment.created).fetch()

        params = {"comments":comments, "u":u}

        return self.render_template("user_comments_list.html", params=params)
