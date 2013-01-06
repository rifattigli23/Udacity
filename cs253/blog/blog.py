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


class BlogHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    
    def render_str(self, template, **params):
        params['user'] = self.user
        return utils.render_str(template, **params)
    
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
    
    def render_json(self, d):
        json_txt = json.dumps(d)
        self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        self.write(json_txt)
    
    def set_secure_cookie(self, name, val):
        cookie_val = utils.make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))
    
    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and utils.check_secure_val(cookie_val)
    
    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))
    
    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')
    
    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))
        
        if self.request.url.endswith('.json'):
            self.format = 'json'
        else:
            self.format = 'html'

def render_post(response, post):
    response.out.write('<b>' + post.subject + '</b><br>')
    response.out.write(post.content)

class MainPage(BlogHandler):
    def get(self):
        self.redirect('/blog')

def age_set(key, val):
    save_time = datetime.utcnow()
    memcache.set(key, (val, save_time))
    
def age_get(key):
    r = memcache.get(key)
    if r:
        val, save_time = r
        age = (datetime.utcnow() - save_time).total_seconds()
    else:
        val, age = None, 0
    
    return val, age

def add_post(post):
    post.put()
    get_posts(update = True)
    return str(post.key().id())
    
def get_posts(update = False):
    q = Post.all().order('-created').fetch(limit = 10)
    mc_key = 'BLOGS'
    
    posts, age = age_get(mc_key)
    if update or posts is None:
        posts = list(q)
        age_set(mc_key, posts)
        
    return posts, age
    
def age_str(age):
    s = 'queried %s seconds ago'
    age = int(age)
    if age == 1:
        s = s.replace('seconds', 'second')
    return s % age    

class BlogFront(BlogHandler):
    def get(self):
        posts, age = get_posts()
        
        if self.format == 'html':
            self.render('front.html', posts = posts
            ,age = age_str(age)
            )
        elif self.format == 'json':
            return self.render_json([p.as_dict() for p in posts])

class PostPage(BlogHandler):
    def get(self, post_id):
        post_key = 'POST_' + post_id
        
        post, age = age_get(post_key)
        
        #if post not returned, lookup from db
        if not post:
            key = db.Key.from_path('Post', int(post_id), parent=utils.blog_key())
            post = db.get(key)
            age_set(post_key, post)
            age = 0
        
        if not post:
            self.error(404)
            return
        
        if self.format == 'html':
            self.render("permalink.html", post = post, age = age_str(age))
        elif self.format == 'json':
            self.render_json(post.as_dict())

class NewPost(BlogHandler):
    def get(self):
        if self.user:
            self.render("newpost.html")
        else:
            self.redirect("/blog/login")
    
    def post(self):
        if not self.user:
            self.redirect('/blog')
        
        subject = self.request.get('subject')
        content = self.request.get('content')
        
        if subject and content:
            p = Post(parent = utils.blog_key(), subject = subject, content = content)
            
            add_post(p)
            
            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = "subject and content, please!"
            self.render("newpost.html", subject = subject, content = content, error = error)

class FlushCache(BlogHandler):
    def get(self):
        if self.request.url.endswith('flush'):
            memcache.flush_all()
        self.redirect('/blog')
    
    
###### Signup Stuff
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Signup(BlogHandler):
    def get(self):
        self.render("signup-form.html")
    
    def post(self):
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')
        
        params = dict(username = self.username,
                      email = self.email)
        
        if not valid_username(self.username):
            params['error_username'] = "That's not a valid username."
            have_error = True
        
        if not valid_password(self.password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif self.password != self.verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True
        
        if not valid_email(self.email):
            params['error_email'] = "That's not a valid email."
            have_error = True
        
        if have_error:
            self.render('signup-form.html', **params)
        else:
            self.done()
    
    def done(self, *a, **kw):
        raise NotImplementedError

class Register(Signup):
    def done(self):
        logging.error("Entered Register.done()")
        
        #make sure the user doesn't already exist
        u = User.by_name(self.username)
        if u:
            msg = 'That user already exists.'
            self.render('signup-form.html', error_username = msg)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()
            
            self.login(u)
            self.redirect('/blog/welcome/?')

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

class Welcome(BlogHandler):            
    def get(self):
        if self.user:
            self.render('welcome.html', username = self.user.name)
        else:
            self.redirect('/blog/signup')            

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
