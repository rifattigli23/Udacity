import os
import re
from string import letters

import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

# Base handler class with utility functions        
class BaseHandler(webapp2.RequestHandler):        
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)    
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

# Define the database model for a Post
class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("blog.html", p = self)
        
# Define the database model for a User
class User(db.Model):
    username = db.StringProperty(required = True)
    password_hash = db.StringProperty(required = True)

# Render all posts
class BlogHandler(BaseHandler):
    def render_front(self, subject="", post="", error=""):
        posts = db.GqlQuery("SELECT * FROM Post "
                            "ORDER BY created DESC ")
        self.render("unit3/blog.html", subject=subject, post=post, error=error, posts=posts)
    
    def get(self):
        self.render_front()

# Submission form    
class NewPostHandler(BaseHandler):
    def render_front(self, subject="", content="", error=""):
        self.render("unit3/newpost.html", subject=subject, content=content, error=error)
    
    def get(self):
        self.render_front()

    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")
        
        if subject and content:
            post = Post(subject=subject, content=content)
            key = post.put()
            self.redirect("/unit3/blog/%d" % key.id())
        else:
            error = "we need both a subject and some content!"
            self.render_front(subject, content, error)
            
# Render a single post
class Permalink(BaseHandler):
    def get(self, post):
        post = Post.get_by_id(int(post))
        self.render("unit3/blog.html", posts = [post])
