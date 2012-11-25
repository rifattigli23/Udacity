import os
import re
from string import letters

import webapp2
import jinja2

import blog

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

class TableOfContents(BaseHandler):
    def get(self):
        self.render('table-of-contents.html')
        
class Play(BaseHandler):
    def get(self):
        self.render('unit1/play.html')
        
class Rot13(BaseHandler):
    def get(self):
        self.render('unit2/rot13-form.html')
        
    def post(self):
        rot13 = ''
        text = self.request.get('text')
        if text:
            rot13 = text.encode('rot13')
        
        self.render('unit2/rot13-form.html', text = rot13)
        
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)
    
class Signup(BaseHandler):

    def get(self):
        self.render("unit2/signup-form.html")
    
    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
            
        params = dict(username = username, 
                      email = email)
        if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True
    
        if not valid_password(password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif password != verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True
    
        if not valid_email(email):
            params['error_email'] = "That's not a valid email."
            have_error = True
    
        if have_error:
            self.render('unit2/signup-form.html', **params)
        else:
            self.redirect('/unit2/welcome?username=' + username)

class Welcome(BaseHandler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.render('unit2/welcome.html', username = username)
        else:
            self.redirect('/unit2/signup')
     
class Art(db.Model):
    title = db.StringProperty(required = True)
    art = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    
           
class AsciiChan(BaseHandler):
    def render_front(self, title="", art="", error=""):
        arts = db.GqlQuery("SELECT * FROM Art "
                            "ORDER BY created DESC ")
        self.render("unit3/front.html", title=title, art=art, error=error, arts=arts)
    
    def get(self):
        self.render_front()
    
    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")
        
        if title and art:
            a = Art(title=title, art=art)
            a.put()
            
            self.redirect("/unit3/asciichan")
        else:
            error = "we need both a title and some artwork!"
            self.render_front(title, art, error)

class Cookies(BaseHandler):
    def get(self):
        self.response.headers['Content-Tpe'] = 'text/plain'
        visits = self.request.cookies.get('visits', '0')
        if visits.isdigit():
            visits = int(visits) + 1
        else:
            visits = 0

        self.response.headers.add_header('Set-Cookie', 'visits=%s' % visits)
        
        if visits > 100:
            self.write("You are the best ever!")
        else:
            self.write("You've been here %s times!" % visits)
            
app = webapp2.WSGIApplication([('/', TableOfContents),
                               ('/unit1/play', Play),
                               ('/unit2/rot13', Rot13),
                               ('/unit2/signup', Signup),
                               ('/unit2/welcome', Welcome),
                               ('/unit3/asciichan', AsciiChan),
                               ('/unit3/blog', blog.BlogHandler),
                               ('/unit3/blog/', blog.BlogHandler),
                               ('/unit3/blog/newpost', blog.NewPostHandler),
                               ('/unit3/blog/newpost/', blog.NewPostHandler),
                               ('/unit3/blog/(\d+)', blog.Permalink),
                               ('/unit4/cookies', Cookies)],
                               debug=True)
