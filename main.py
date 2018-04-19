#!/usr/bin/env python

import webapp2

from handlers.base import MainHandler, CookieAlertHandler
from handlers.comments import CommentAdd, CommentsList, CommentDelete, UserCommentsList, EditComment
from handlers.topics import TopicAdd, TopicDetails, TopicDelete, UserTopicList, EditTopic
from handlers.users import UsersHandler
from workers.email_new_comment import EmailNewCommentWorker
from crons.delete_topics import DeleteTopicsCron
from crons.delete_comments import DeleteCommentsCron
from crons.send_email_subscribers import SendEmailSubscribersCron


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main-page"),
    webapp2.Route('/set-cookie', CookieAlertHandler, name="set-cookie"),

    webapp2.Route('/topic/add', TopicAdd, name="topic-add"),
    webapp2.Route('/topic/<topic_id:\d+>/details', TopicDetails, name="topic-details"),
    webapp2.Route('/users', UsersHandler),
    webapp2.Route('/topic/<topic_id:\d+>/comment/add', CommentAdd, name="comment-add"),
    webapp2.Route('/topic/<topic_id:\d+>/delete', TopicDelete, name="topic-delete"),
    webapp2.Route('/comment/<comment_id:\d+>/delete', CommentDelete, name="comment-delete"),

    webapp2.Route('/topic/<topic_id:\d+>/edit', EditTopic, name="edit-topic"),
    webapp2.Route('/comment/<comment_id:\d+>/edit', EditComment, name="edit-comment"),

    webapp2.Route('/comments/list', CommentsList, name="comment-list"),
    webapp2.Route('/user/<user_id:\d+>/user_topic_list', UserTopicList, name="user-topic-list"),
    webapp2.Route('/user/<user_id:\d+>/user_comments_list', UserCommentsList, name="user-comments-list"),

    webapp2.Route('/task/email-new-comment', EmailNewCommentWorker, name="task-email-new-comment"),

    webapp2.Route("/cron/delete-topics", DeleteTopicsCron, name="cron-delete-topics"),
    webapp2.Route("/cron/delete-comments", DeleteCommentsCron, name="cron-delete-comments"),

    webapp2.Route('/cron/send-email', SendEmailSubscribersCron, name="cron-send-email"),

], debug=True)
