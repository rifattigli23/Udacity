from MainHandler import MainHandler
from lib import utils
from google.appengine.ext import db


class NewWiki(MainHandler):
    def get(self, page_name):
        wiki_key = 'WIKI_' + page_name 
        wiki, age = utils.age_get(wiki_key)
        
        #if wiki not returned by memcached, lookup from db
        if not wiki:
            key = db.Key.from_path('Wiki', page_name, parent=utils.wiki_key())        
            wiki = db.get(key)
            
            utils.age_set(wiki_key, wiki)
            age = 0    
        
        if wiki:
            #if url exists, redirect to WikiPage
            self.params['wiki'] = wiki
            self.params['age'] = 'AGE PLACEHOLDER'
            self.render("wiki-page.html")
        else:
            #if url doesn't exist, redirect to WikiEdit.py
            self.redirect('/_edit%s' % page_name)
            return