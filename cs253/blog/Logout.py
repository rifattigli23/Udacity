from BlogHandler import BlogHandler

class Logout(BlogHandler):
    def get(self):
        self.logout()
        self.redirect('/blog/signup') #TODO change redirect to /blog