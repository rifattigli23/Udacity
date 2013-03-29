## Udacity CS101 Web Crawler
import urllib2
    
##
#   Utilities
##    
def union(a,b):
    return list(set(a+b))

def split_string(source,splitlist):    
    default_sep = splitlist[0]
    for sep in splitlist[1:]:
        source = source.replace(sep, default_sep)
    return [i.strip() for i in source.split(default_sep) if i != '']

    
##
#   Index Stuff
##    
def lookup(index,keyword):
    for entry in index:
        if (entry[0] == keyword):
            return entry[1]
    return []
    
def record_user_click(index,keyword,url):
    for entry in index:
        if entry[0] == keyword:
            for element in entry[1]:
                if element[0] == url:
                    element[1] += 1

def add_to_index(index, keyword, url):
    # loop through existing keywords
    for entry in index:
        # check if current keyword matches our parameter value
        if entry[0] == keyword:
            # loop through existing url-count lists
            for url_and_count in entry[1]:
                if url_and_count[0] == url:
                    return
            # if we leave loop, url does not yet exist, so append it
            entry[1].append([url, 0])
            return
    # not found, add new keyword to index
    index.append([keyword, [[url, 0]]])  

def add_page_to_index(index,url,content):
    contentList = content.split()
    
    for keyword in contentList:
        add_to_index(index, keyword, url)

##
#   Crawl Stuff
##
def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote+1:end_quote]
    return url, end_quote
        
def get_all_links(page):
    links = []
    while get_next_target(page)[0] != None:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

def get_page(url):
    try:
        import urllib
        return urllib.urlopen(url).read()
    except:
        return ""
    
def crawl(seed):
    tocrawl = [seed]
    crawled = []
    index = []
    
    while tocrawl:
        next_crawl = tocrawl.pop()
        if next_crawl not in crawled:
            page = get_page(next_crawl)
            add_page_to_index(index,next_crawl,page)
            page_links = get_all_links(page)
            union(tocrawl, page_links)
        crawled.append(next_crawl)
    return index

seed = 'http://www.udacity.com/cs101x/index.html'

print crawl(seed)