###
### search.py
###

from webcorpus import WebCorpus

def lucky_search(corpus, keyword):

    pages = corpus.lookup(keyword)
    
    if not pages:
        return None
    best_page = pages[0]
    best_rank = corpus.page_rank(best_page)
    
    for candidate in pages:
        if corpus.page_rank(candidate) > best_rank:
                best_page = candidate
                best_rank = corpus.page_rank(candidate)
    return best_page

def quicksort_pages(corpus, pages):
    if not pages or len(pages) <= 1:
        return pages
    else:
        pivot = corpus.page_rank(pages[0])
        worse = []
        better = []
        for page in pages[1:]:
            if corpus.page_rank(page) <= pivot:
                worse.append(page)
            else:
                better.append(page)
        return quicksort_pages(corpus, better) + [pages[0]] + quicksort_pages(corpus, worse)
            
def ordered_search(corpus, keyword):
    pages = corpus.lookup(keyword)
    return quicksort_pages(corpus, pages)
