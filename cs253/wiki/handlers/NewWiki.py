from MainHandler import MainHandler
from lib import utils
from google.appengine.ext import db
from lib.db.Wiki import Wiki
import logging

class NewWiki(MainHandler):
    def get(self, page_name):
        wiki_key = 'WIKI_' + page_name 
        wiki, age = utils.age_get(wiki_key)
        
        # wiki = Wiki.memcached_get(page_name)
        
        #if wiki not returned by memcached, lookup from db
        if not wiki:
            # key = db.Key.from_path('Wiki', page_name, parent=utils.wiki_key())        
            # wiki = db.get(key)
            
            #get wiki from db via gql query 
            query = Wiki.gql("WHERE name =:page_name ORDER BY created desc LIMIT 1", page_name = page_name)
            wikis = query.fetch(limit=1)
            wiki = wikis[0]
            
            utils.age_set(wiki_key, wiki)
            age = 0    

        #if url exists, render to WikiPage        
        if wiki:
            self.params['wiki'] = wiki
            self.params['age'] = utils.age_str(age)
            self.render("wiki-page.html")
            logging.error(Wiki.get_all_versions(page_name))

        #if url doesn't exist and user is logged in, redirect to WikiEdit.py
        elif not wiki and self.user:
            self.redirect('/_edit%s' % page_name)
            return
        
        #if url doesn't exist and user is NOT logged in, redirect to login
        else:
            self.redirect('/login')