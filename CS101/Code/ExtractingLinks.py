## Udacity CS101 Web Crawler
import urllib2

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
    usock = urllib2.urlopen(url)
    html = usock.read()
    usock.close()
    return html

def crawl(seed):
    tocrawl = [seed]
    crawled = []
    
    while tocrawl:
        next_crawl = tocrawl.pop()
        if next_crawl not in crawled:
            page = get_page(next_crawl)
            page_links = get_all_links(page)
            tocrawl += page_links
        crawled.append(next_crawl)
    return crawled

seed = 'http://www.udacity.com/cs101x/index.html'

print crawl(seed)