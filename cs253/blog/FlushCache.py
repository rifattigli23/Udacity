from BlogHandler import BlogHandler
from google.appengine.api import memcache


class FlushCache(BlogHandler):
    def get(self):
        if self.request.url.endswith('flush'):
            memcache.flush_all()
        self.redirect('/blog')