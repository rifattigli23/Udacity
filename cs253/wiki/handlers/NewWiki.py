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

        #if url exists, redirect to WikiPage        
        if wiki:
            self.params['wiki'] = wiki
            self.params['age'] = 'AGE PLACEHOLDER' #TODO: add memcached age
            self.render("wiki-page.html")

        #if url doesn't exist and user is logged in, redirect to WikiEdit.py
        elif not wiki and self.user:
            self.redirect('/_edit%s' % page_name)
            return
        
        #if url doesn't exist and user is NOT logged in, redirect to login
        else:
            self.redirect('/login')