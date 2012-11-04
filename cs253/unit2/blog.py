import os
import re
from string import letters

import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)
        
class BaseHandler(webapp2.RequestHandler):        
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))
        
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    
class Blog(db.Model):
    title = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class Blog(BaseHandler):
    def render_front(self, title="", content="", error=""):
        contents = db.GqlQuery("SELECT * FROM content "
                            "ORDER BY created DESC ")
        self.render("unit3/blog.html", title=title, content=content, error=error, contents=contents)
    
    def get(self):
        self.render_front()
    
    def post(self):
        title = self.request.get("title")
        content = self.request.get("content")
        
        if title and content:
            a = content(title=title, content=content)
            a.put()
            
            self.redirect("/unit3/blog")
        else:
            error = "we need both a title and some content!"
            self.render_front(title, content, error)
        
