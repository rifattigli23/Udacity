from MainHandler import MainHandler
from lib import utils
from lib.db.Wiki import Wiki
import logging

#:TODO: add in user login checks before displaying content

def add_wiki(wiki):
    wiki.put()
    # Wiki.get_wikis(update = True) #TODO: add memcache updating
    return str(wiki.key().id())

class WikiEdit(MainHandler):
    def get(self, page_name):
        logging.error(page_name)
        wiki_key = 'WIKI_' + page_name 
        wiki, age = utils.age_get(wiki_key)
        content = str()
        if wiki:
            content = wiki.content
        
        self.params['content'] = content
        self.render('wiki-edit.html')

    def post(self, page_name):
        content = self.request.get('content')
        parent = utils.wiki_key()
               
        if content:
            w = Wiki(parent = parent, key_name = page_name, name = page_name, content = content)
                   
            add_wiki(w)
            self.redirect('%s%s' % (utils.domain_host, page_name))
        else:
            self.write("Oops...we screwed up. Sorry about that!")