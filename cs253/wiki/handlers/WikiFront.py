from MainHandler import MainHandler

class WikiFront(MainHandler):
    def get(self):
        # self.make_logged_out_header(self, page_name)
        self.render('wiki-front.html')