from BlogHandler import BlogHandler
from BlogFront import BlogFront
from PostPage import PostPage
from NewPost import NewPost
from Register import Register
from Login import Login
from Logout import Logout
from Welcome import Welcome
from FlushCache import FlushCache

import webapp2

class MainPage(BlogHandler):
    def get(self):
        self.redirect('/blog')

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/blog/?(?:\.json)?', BlogFront),
                               ('/blog/([0-9]+)(?:\.json)?', PostPage),
                               ('/blog/newpost/?', NewPost),
                               ('/blog/signup/?', Register),
                               ('/blog/login/?', Login),
                               ('/blog/logout/?', Logout),
                               ('/blog/welcome/?', Welcome),
                               ('/blog/flush/?', FlushCache)
                               ],
                              debug=True)