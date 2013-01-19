from handlers.MainHandler import MainHandler
from handlers.Register import Register
from handlers.Login import Login
from handlers.Logout import Logout
from handlers.FlushCache import FlushCache
from handlers.WikiFront import WikiFront
from handlers.NewWiki import NewWiki
from handlers.WikiEdit import WikiEdit

import webapp2

PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'

app = webapp2.WSGIApplication([
                               ('/signup/?', Register),
                               ('/login/?', Login),
                               ('/logout/?', Logout),
                               ('/flush/?', FlushCache),
                               ('/', WikiFront),
                               ('/_edit' + PAGE_RE, WikiEdit),
                               (PAGE_RE, NewWiki)
                               ],
                              debug=True)