from MainHandler import MainHandler

class Welcome(MainHandler):            
    def get(self):
        if self.user:
            self.render('welcome.html', username = self.user.name)
        else:
            self.redirect('/blog/signup')  