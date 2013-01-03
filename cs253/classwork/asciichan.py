import basehandler
from google.appengine.ext import db
import urllib2
from xml.dom import minidom

GMAPS_URL = "http://maps.googleapis.com/maps/api/staticmap?size=380x263&sensor=false&"
def gmaps_img(points):
    markers = '&'.join('markers=%s,%s' % (p.lat, p.lon)
                        for p in points)
    return GMAPS_URL + markers

def get_coords(ip):
    ip = "4.2.2.2" #TODO: comment out, for development only
    ip = "23.24.209.141" #TODO: comment out, for development only
    IP_URL ="http://api.hostip.info/?ip="
    url = IP_URL + ip
    content = None

    try:
        content = urllib2.urlopen(url).read()
    except URLError:
        return
        
    if content:
        dom = minidom.parseString(content)
        coordinateNodeList = dom.getElementsByTagName('gml:coordinates')
        if coordinateNodeList and coordinateNodeList[0].firstChild.nodeValue:
            lon , lat = coordinateNodeList[0].firstChild.nodeValue.split(',')
            return db.GeoPt(lat, lon)

class Art(db.Model):
    title = db.StringProperty(required = True)
    art = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    coordinates = db.GeoPtProperty()

class AsciiChan(basehandler.BaseHandler):
    def render_front(self, title="", art="", error=""):
        arts = db.GqlQuery("SELECT * FROM Art "
                            "ORDER BY created DESC ")
        
        #prevent the running of multiple queries
        arts = list(arts)

        #find which arts have coords        
        points = filter(None, (a.coordinates for a in arts))

        # if we have any arts with coords, make an image url
        img_url = None
        if points:
            img_url = gmaps_img(points)

        #display the image url
        self.render("front.html", title=title, art=art, 
                    error=error, arts=arts, img_url = img_url)

    def get(self):
        self.render_front()
    
    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")
        #lookup the user's coordiantes from their IP
        coords = get_coords(self.request.remote_addr)

        if title and art:
            a = Art(title=title, art=art)
            
            #if we have coordinates, add them to the Art
            if coords:
                a.coordinates = coords
            
            a.put()
            self.redirect("/unit3/asciichan")
        else:
            error = "we need both a title and some artwork!"
            self.render_front(title, art, error)
            
# TODO: add map to the front page
    # use hostip.info to lookup location data for ip addresses
# TODO: draw a map
    # Google Maps (static maps)