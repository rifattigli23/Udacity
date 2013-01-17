from MainHandler import MainHandler
from lib import utils
from lib.db.Post import Post

class BlogFront(MainHandler):
    def get(self):
        posts, age = Post.get_posts()
        age_str = utils.age_str(age)
        
        if self.format == 'html':
            self.render('front.html', posts = posts, age = age_str)
        elif self.format == 'json':
            return self.render_json([p.as_dict() for p in posts])