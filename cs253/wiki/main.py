from handlers.MainHandler import MainHandler
from handlers.Register import Register
from handlers.Login import Login
from handlers.Logout import Logout
from handlers.FlushCache import FlushCache
from handlers.WikiFront import WikiFront
from handlers.NewWiki import NewWiki
from handlers.WikiEdit import WikiEdit

import webapp2

app = webapp2.WSGIApplication([
                               ('/blog/signup/?', Register),
                               ('/blog/login/?', Login),
                               ('/blog/logout/?', Logout),
                               ('/blog/flush/?', FlushCache),
                               ('/', WikiFront),
                               ('/_edit/(.*)/?', WikiEdit),
                               ('/(.*)/?', NewWiki)
                               ],
                              debug=True)