from BlogHandler import BlogHandler
from lib import utils
from google.appengine.ext import db

class PostPage(BlogHandler):
    def get(self, post_id):
        post_key = 'POST_' + post_id
        
        post, age = utils.age_get(post_key)
        
        #if post not returned, lookup from db
        #TODO: move db logic to utils or Post
        if not post:
            key = db.Key.from_path('Post', int(post_id), parent=utils.blog_key())
            post = db.get(key)
            utils.age_set(post_key, post)
            age = 0
        
        if not post:
            self.error(404)
            return
        
        if self.format == 'html':
            self.render("permalink.html", post = post, age = utils.age_str(age))
        elif self.format == 'json':
            self.render_json(post.as_dict())