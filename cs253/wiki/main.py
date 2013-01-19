from handlers.MainHandler import MainHandler
from handlers.Signup import Signup
from handlers.Login import Login
from handlers.Logout import Logout
from handlers.FlushCache import FlushCache
from handlers.NewWiki import NewWiki
from handlers.WikiEdit import WikiEdit
from handlers.WikiHistory import WikiHistory

import webapp2

PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'

app = webapp2.WSGIApplication([
                               ('/signup/?', Signup),
                               ('/login/?', Login),
                               ('/logout/?', Logout),
                               ('/flush/?', FlushCache),
                               ('/_history' + PAGE_RE, WikiHistory),
                               ('/_edit' + PAGE_RE, WikiEdit),
                               (PAGE_RE, NewWiki)
                               ],
                              debug=True)