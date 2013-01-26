from MainHandler import MainHandler
from lib.db.Wiki import Wiki

class WikiHistory(MainHandler):
    def get(self, page_name):
        all_wiki_versions = Wiki.get_all_versions(page_name)
        self.params['wikis'] = all_wiki_versions
        self.render('wiki-history.html')