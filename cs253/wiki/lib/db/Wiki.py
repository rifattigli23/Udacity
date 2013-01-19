from lib import utils
from google.appengine.ext import db

class Wiki(db.Model):
    name = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)
    
    def render(self):
        c = self.content.replace('\n', '<br>')
        return c