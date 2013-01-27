from MainHandler import MainHandler
from lib import utils
from google.appengine.ext import db
from lib.db.Wiki import Wiki
import logging

class NewWiki(MainHandler):
    def get(self, page_name):

        # if version requested, return appropriate wiki version
        version = self.request.get('v', '')
        logging.error('WIKI VERSION REQUEST = ' + version)

        #MEMCACHED DISABLED
        wiki = ''
        wiki_key = ''
        # wiki_key = 'WIKI_' + page_name 
        # wiki, age = utils.age_get(wiki_key)
                
        #if wiki not returned by memcached, lookup from db
        if not wiki:
            #get wiki from db via gql query 
            
            if version != '':
                query = Wiki.gql("WHERE name =:page_name AND version =:version ORDER BY created desc LIMIT 1", page_name = page_name, version = int(version))
            else:            
                query = Wiki.gql("WHERE name =:page_name ORDER BY created desc LIMIT 1", page_name = page_name)

            wikis = query.fetch(limit=1)
            
            if len(wikis) > 0:
                wiki = wikis[0]
                logging.error('WIKI VERSION ACTUAL = ' + str(wiki.version))
                utils.age_set(wiki_key, wiki)
                age = 0               

        #if wiki exists, render WikiPage        
        if wiki:            
            self.params['wiki'] = wiki
            self.params['age'] = utils.age_str(age)
            self.render("wiki-page.html")

        #if wiki doesn't exist and user is logged in, redirect to WikiEdit.py
        elif not wiki and self.user:
            self.redirect('/_edit%s' % page_name)
            return
        
        #if url doesn't exist and user is NOT logged in, redirect to login
        else:
            self.redirect('/login')