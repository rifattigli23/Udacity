from Signup import Signup
from lib.db.User import User

class Register(Signup):
    def done(self):        
        #make sure the user doesn't already exist
        u = User.by_name(self.username)
        if u:
            msg = 'That user already exists.'
            self.params['error_username'] = msg
            self.render('signup-form.html')
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()
            
            self.login(u)
            self.redirect('/welcome/?')