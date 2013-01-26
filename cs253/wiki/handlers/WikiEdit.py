from MainHandler import MainHandler
from lib import utils
from lib.db.Wiki import Wiki

#:TODO: add in user login checks before displaying content

def add_wiki(wiki):
    wiki.put()
    wiki.memcached_put()
    return str(wiki.key().id())

class WikiEdit(MainHandler):
    def get(self, page_name):
        # wiki_key = 'WIKI_' + page_name 
        #         wiki, age = utils.age_get(wiki_key)
        wiki = Wiki.memcached_get(page_name)
        content = str()
        if wiki:
            content = wiki.content
        
        self.params['content'] = content
        self.render('wiki-edit.html')

    def post(self, page_name):
        content = self.request.get('content')
        parent = utils.wiki_key()
        w = Wiki(parent = parent, name = page_name, content = content)  
        add_wiki(w)
        self.redirect(page_name)