from google.appengine.ext import ndb

class Topic(ndb.Model):
    title = ndb.StringProperty()
    content = ndb.TextProperty()
    author_email = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    deleted = ndb.BooleanProperty(default=False)

    @classmethod
    def create(cls, title, content, user,):
        new_topic = cls(title=title, content=content, author_email=user.email())
        new_topic.put()

        return new_topic

    @classmethod
    def delete(cls, topic):
        topic.deleted = True
        topic.put()

        return topic
