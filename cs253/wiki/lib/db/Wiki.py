from lib import utils
from google.appengine.ext import db

MEMCACHED_PREFIX = 'WIKI_'

class Wiki(db.Model):
    name = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)
    version = db.IntegerProperty(required = True)
    #TODO: add version property, URI Routing for ?v variable, and query logic to retreive the correct version 
    #following the "view" link on the history pagek
    
    def render(self):
        c = self.content.replace('\n', '<br>')
        return c
    
    def render_version_row(self):
        return utils.render_str("wiki-history-row.html", w = self)
    
    def memcached_put(self):
        utils.age_set(MEMCACHED_PREFIX + self.name, self)
        
    @classmethod    
    def memcached_get(cls, page_name):
        wiki, age = utils.age_get(MEMCACHED_PREFIX + page_name)
        return wiki
    
    @classmethod
    def get_all_versions(cls, page_name, update = False):
        # q = Wiki.all().order('-created').fetch(limit = 10)
        # q = Wiki.get_by_key_name(page_name, parent = utils.wiki_key()).order('-created')
        mc_key = page_name + '_VERSIONS'

    
        wikis, age = utils.age_get(mc_key)
        if update or wikis is None:
            # wikis = list(q)
            q = Wiki.gql("WHERE name = :name ORDER BY created DESC", name=page_name)
            wikis = q.fetch(limit = None)
            
            utils.age_set(mc_key, wikis)
            
        return wikis
        
    @classmethod
    def get_max_version(cls, page_name, update = False):
        versions = cls.get_all_versions(page_name, update)
        if len(versions) > 0:
            # versions should be ordered by descending created times
            return versions[0]
            
            
        
        
        
        