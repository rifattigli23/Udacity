from lib import utils
from google.appengine.ext import db

MEMCACHED_PREFIX = 'WIKI_'

class Wiki(db.Model):
    name = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)
    
    def render(self):
        c = self.content.replace('\n', '<br>')
        return c
    
    def render_version_row(self):
        return utils.render_str("wiki-history-row.html", w = self)
    
    def memcached_put(self):
        # overwrite "current" memcached version without version name in key (one for each name)
        utils.age_set(MEMCACHED_PREFIX + self.name, self)

        # set value for memcached key with version
        utils.age_set(MEMCACHED_PREFIX + self.name + str(self.key().id()), self)
        
        
    @classmethod    
    def memcached_get(cls, page_name, version=''):
        wiki, age = utils.age_get(MEMCACHED_PREFIX + page_name + version)
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
            
            
        
        
        
        