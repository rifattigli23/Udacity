from MainHandler import MainHandler
import re

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

class Signup(MainHandler):
    def get(self):
        self.render("signup-form.html")
    
    def post(self):
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')
        
        self.params['username'] = self.username
        self.params['email'] = self.email
        
        if not valid_username(self.username):
            self.params['error_username'] = "That's not a valid username."
            have_error = True
        
        if not valid_password(self.password):
            self.params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif self.password != self.verify:
            self.params['error_verify'] = "Your passwords didn't match."
            have_error = True
        
        if not valid_email(self.email):
            self.params['error_email'] = "That's not a valid email."
            have_error = True
        
        if have_error:
            self.render('signup-form.html')
        else:
            self.done()
    
    def done(self, *a, **kw):
        raise NotImplementedError