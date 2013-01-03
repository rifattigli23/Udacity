import json
import urllib2

reddit_front = urllib2.urlopen("http://www.reddit.com/.json").read() 

# QUIZ - reddit_front is a JSON string of reddit's front page. Inside it is a
# list of links, each of which has an "ups" attribute. From this dataset, what
# is the total number of ups of all the links?
#
# Implement the function total_ups(), and make it return the total number of ups.
# This is going to require some experimental searching through the reddit_front 
# JSON, which is a fairly typical problem when dealing with APIs, RSS, or JSON. 
# You'll need to load the json using the json.loads method, after which you 
# should be able to search through the json similarly to a dictionary or list. 
# Note that you will need to access parts of the JSON as a dictionary, and 
# others as a list.
# You can also try running this in the python interpreter in the console, 
# which may make it easier to search through reddit_front.

def total_ups():
    j = json.loads(reddit_front)
    return sum(c['data']['ups'] for c in j['data']['children'])

print 'total ups = ' + str(total_ups())