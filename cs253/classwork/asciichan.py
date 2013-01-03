import basehandler
from google.appengine.ext import db
import urllib2
from xml.dom import minidom

class Art(db.Model):
    title = db.StringProperty(required = True)
    art = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class AsciiChan(basehandler.BaseHandler):
    def render_front(self, title="", art="", error=""):
        arts = db.GqlQuery("SELECT * FROM Art "
                            "ORDER BY created DESC ")
        self.render("front.html", title=title, art=art, error=error, arts=arts)
    
    def get_coords(ip):
        IP_URL ="http://api.hostip.info/?ip="
        url = IP_URL + ip
        content = None

        try:
            content = url2lib2.urlopen(url).read()
        except URLError:
            return
        
        if content:
            #parse the xml and find the coordinates
            dom = minidom.parseString(content)
            coordinateNodeList = dom.getElementsByTagName('gml:coordinates')
            lon , lat = coordinateNodeList[0].firstChild.nodeValue.split(',')
            return lat, lon
    
    def get(self):
        self.render_front()
    
    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")
        
        if title and art:
            a = Art(title=title, art=art)
            
            #lookup the user's coordiantes from their IP
            #if we have coordinates, add them to the Art
            
            
            a.put()
            self.redirect("/unit3/asciichan")
        else:
            error = "we need both a title and some artwork!"
            self.render_front(title, art, error)
            
# TODO: add map to the front page
    # use hostip.info to lookup location data for ip addresses
# TODO: draw a map
    # Google Maps (static maps)