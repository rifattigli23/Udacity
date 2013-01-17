from MainHandler import MainHandler
from lib import utils
from lib.db.Post import Post
import logging

def add_post(post):
    post.put()
    Post.get_posts(update = True)
    return str(post.key().id())

class NewPost(MainHandler):
    def get(self):
        if self.user:
            self.render("newpost.html")
        else:
            self.redirect("/blog/login")
    
    def post(self):
        logging.error(utils.blog_key())
        if not self.user:
            self.redirect('/blog')

        subject = self.request.get('subject')
        content = self.request.get('content')
        parent = utils.blog_key()

        if subject and content:
            logging.error(utils.age_str(12345))
            p = Post(parent = parent, subject = subject, content = content)
                    
            add_post(p)
                    
            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = "subject and content, please!"
            self.render("newpost.html", subject = subject, content = content, error = error)
