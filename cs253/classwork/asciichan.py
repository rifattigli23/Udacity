import basehandler
from google.appengine.ext import db
import urllib2
from xml.dom import minidom

class Art(db.Model):
    title = db.StringProperty(required = True)
    art = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class AsciiChan(basehandler.BaseHandler):
    def render_front(self, title="", art="", error=""):
        arts = db.GqlQuery("SELECT * FROM Art "
                            "ORDER BY created DESC ")
        self.render("front.html", title=title, art=art, error=error, arts=arts)
    
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