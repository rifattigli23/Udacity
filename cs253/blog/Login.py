from BlogHandler import BlogHandler
from lib.db.User import User

class Login(BlogHandler):
    def get(self):
        self.render('login-form.html')
    
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        
        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/blog/welcome/?')
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error = msg)