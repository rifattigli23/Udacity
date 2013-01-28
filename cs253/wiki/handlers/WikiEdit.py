from MainHandler import MainHandler
from lib import utils
from lib.db.Wiki import Wiki

#:TODO: add in user login checks before displaying content

def add_wiki(wiki):
    wiki.put()
    wiki.memcached_put()
    Wiki.get_all_versions(wiki.name, update = True)
    return str(wiki.key().id())

class WikiEdit(MainHandler):
    def get(self, page_name):
        version = self.request.get('v', None)
        
        if version:
            wiki = Wiki.memcached_get(page_name, version)            
        else:
            wiki = Wiki.memcached_get(page_name)
        content = str()
        if wiki:
            content = wiki.content
        
        self.params['content'] = content
        self.render('wiki-edit.html')

    def post(self, page_name):
        content = self.request.get('content')
        parent = utils.wiki_key()
        
        #TODO: replace this version logic with use of Google's auto incrementing IDs
        max_version = Wiki.get_max_version(page_name, update = True)
        if max_version:
            version = max_version.version + 1
        else:
            version = 1
            
        w = Wiki(parent = parent, name = page_name, content = content, version = version)  
        add_wiki(w)
        self.redirect(page_name)