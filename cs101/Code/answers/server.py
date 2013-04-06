import web

from search import lucky_search
from crawler import crawl_web

class LuckySearch(object):
    def GET(self, query):
        return lucky_search(corpus, query)
        
corpus = crawl_web('http://udacity.com/cs101x/urank/index.html')
app = web.application(('/(.*)', 'LuckySearch'), globals())
app.run()