import web

from search import lucky_search
from crawler import crawl_web

class LuckySearch(object):
    def GET(self, query):
        res = lucky_search(corpus, query)
        if res == None:
            return 'Try searchwithpeter.info'
        else:
            return res
        
class About(object):
    def GET(self):
        return 'This is my udacious project!'


        # return 'This is my udacious project!'
        
corpus = crawl_web('http://udacity.com/cs101x/urank/index.html')
urls = (
    
)
app = web.application(('/about', 'About', '/(.*)', 'LuckySearch'), globals())
app.run()