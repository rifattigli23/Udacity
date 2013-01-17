from MainHandler import MainHandler
from BlogFront import BlogFront
from PostPage import PostPage
from NewPost import NewPost
from Register import Register
from Login import Login
from Logout import Logout
from Welcome import Welcome
from FlushCache import FlushCache
from WikiFront import WikiFront
from NewWiki import NewWiki
from WikiEdit import WikiEdit

import webapp2

class MainPage(MainHandler):
    def get(self):
        self.redirect('/blog')

app = webapp2.WSGIApplication([
                               # ('/', MainPage),
                               ('/blog/?(?:\.json)?', BlogFront),
                               ('/blog/([0-9]+)(?:\.json)?', PostPage),
                               ('/blog/newpost/?', NewPost),
                               ('/blog/signup/?', Register),
                               ('/blog/login/?', Login),
                               ('/blog/logout/?', Logout),
                               ('/blog/welcome/?', Welcome),
                               ('/blog/flush/?', FlushCache),
                               ('/', WikiFront),
                               ('/_edit/(.*)/?', WikiEdit),
                               ('/(.*)/?', NewWiki)
                               ],
                              debug=True)