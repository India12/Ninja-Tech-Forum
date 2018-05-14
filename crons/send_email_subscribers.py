import datetime
from models.user import User
from models.topic import Topic
from handlers.base import BaseHandler
from google.appengine.api import mail

class SendEmailSubscribersCron(BaseHandler):
    def get(self):

        users = User.query(User.is_subscribed == True).fetch()
        added_topics = Topic.query(Topic.deleted == False,
                        Topic.created > datetime.datetime.now() - datetime.timedelta(days=1)).fetch()


        for user in users:
            mail.send_mail(subject="Topics added in last 24 hours",
                            sender="turnsek.lucija@gmail.com",
                            to=user.email,
                            body="test")

'''if added_topics:
    topic_link = ""
    for topic in added_topics:
        topic_link += topic.title + "- " + str(topic.key.id()) + " , "
        #topic_link += topic.title + "- " + "http://wd2-forum-lucija.appspot.com/topic/" + str(topic.key.id()) + " , "
'''
'''body="Topics: %s" % topic_link)'''
