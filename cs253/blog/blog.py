import re
import json
from time import strftime
import time
from google.appengine.api import memcache
import logging
from datetime import datetime, timedelta

import webapp2

from google.appengine.ext import db

from lib.db.User import User
from lib.db.Post import Post
from lib import utils
from BlogHandler import BlogHandler
from BlogFront import BlogFront
from Signup import Signup
from Register import Register
from FlushCache import FlushCache
from Welcome import Welcome
from NewPost import NewPost

# def render_post(response, post):
#     response.out.write('<b>' + post.subject + '</b><br>')
#     response.out.write(post.content)

class MainPage(BlogHandler):
    def get(self):
        self.redirect('/blog')

class PostPage(BlogHandler):
    def get(self, post_id):
        post_key = 'POST_' + post_id
        
        post, age = utils.age_get(post_key)
        
        #if post not returned, lookup from db
        if not post:
            key = db.Key.from_path('Post', int(post_id), parent=utils.blog_key())
            post = db.get(key)
            utils.age_set(post_key, post)
            age = 0
        
        if not post:
            self.error(404)
            return
        
        if self.format == 'html':
            self.render("permalink.html", post = post, age = utils.age_str(age))
        elif self.format == 'json':
            self.render_json(post.as_dict())


class Login(BlogHandler):
    def get(self):
        self.render('login-form.html')
    
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        
        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/blog/welcome/?')
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error = msg)

class Logout(BlogHandler):
    def get(self):
        self.logout()
        self.redirect('/blog/signup') #TODO change redirect to /blog


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/blog/?(?:\.json)?', BlogFront),
                               ('/blog/([0-9]+)(?:\.json)?', PostPage),
                               ('/blog/newpost/?', NewPost),
                               ('/blog/signup/?', Register),
                               ('/blog/login/?', Login),
                               ('/blog/logout/?', Logout),
                               ('/blog/welcome/?', Welcome),
                               ('/blog/flush/?', FlushCache)
                               ],
                              debug=True)
