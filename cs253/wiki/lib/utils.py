import os
import jinja2
import hmac
from google.appengine.ext import db
from google.appengine.api import memcache
from datetime import datetime, timedelta

template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

secret = 'ohSoSecret'

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

def make_secure_val(val):
    return'%s|%s' % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val
        
##### blog stuff
def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)
    
##### wiki stuff
def wiki_key(name = 'default'):
    return db.Key.from_path('wikis', name)
    
##### memcached stuff
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
    
def age_str(age):
    s = 'queried %s seconds ago'
    age = int(age)
    if age == 1:
        s = s.replace('seconds', 'second')
    return s % age    