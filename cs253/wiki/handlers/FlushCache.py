from MainHandler import MainHandler
from google.appengine.api import memcache


class FlushCache(MainHandler):
    def get(self):
        if self.request.url.endswith('flush'):
            memcache.flush_all()
        self.redirect('/blog')