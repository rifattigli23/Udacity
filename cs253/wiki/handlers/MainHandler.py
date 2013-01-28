import webapp2
from lib import utils
from lib.db.User import User
import logging  

class MainHandler(webapp2.RequestHandler):
    
    params = {} ## params contains key-value pairs used by jinja2 templates to render all html
    
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    
    def render_str(self, template):
        self.params['user'] = self.user
        return utils.render_str(template, **self.params)
    
    def render(self, template):
        self.write(self.render_str(template))
    
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
        self.user = user
        self.make_logged_in_header()
    
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
            
        if self.user:
            self.make_logged_in_header()
        else:
            self.make_logged_out_header()

    def make_logged_out_header(self):
        page = self.request.path
        history_link = '/_history' + page
        self.params['history'] = '<a href="%s">hisotry</a>' % history_link
        self.params['auth'] = '<a href="/login">login</a>|<a href="/signup">signup</a>'
        self.params['edit'] = ''
        
    def make_logged_in_header(self):
        page = self.request.path
        history_link = '/_history' + page
        
        if self.request.get('v', None):
            self.params['edit'] = '<a href="_edit%s?v=%s">edit</a>' % (page, self.request.get('v'))
        else:
            self.params['edit'] = '<a href="_edit%s">edit</a>' % page
        self.params['history'] = '<a href="%s">history</a>' % history_link
        self.params['auth'] = self.user.name + '(<a href="/logout">logout</a>)'
        logging.error(self.request.path)
        
        if '_edit' in self.request.path:
            # view wiki entry
            self.params['edit'] = '<a href="%s">view</a>' % page.replace('_edit/', '')
        
        if '_history' in self.request.path:
            self.params['edit'] = ''
            self.params['history'] = ''