from lib import utils
from google.appengine.ext import db

MEMCACHED_PREFIX = 'WIKI_'

class Wiki(db.Model):
    name = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)
    
    def render(self):
        c = self.content.replace('\n', '<br>')
        return c
    
    
    
    def memcached_put(self):
        utils.age_set(MEMCACHED_PREFIX + self.name, self)
        
    @classmethod    
    def memcached_get(cls, page_name):
        wiki, age = utils.age_get(MEMCACHED_PREFIX + page_name)
        return wiki