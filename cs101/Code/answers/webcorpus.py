"""
Next, we want to improve the modularity of our search engine code by making the WebCorpus abstract.  

The attributes index, graph, and ranks should no longer be used outside the webcorpus module.  
To indicate this, rename them following the convention of using an underscore at the beginning of private attributes.  
(Python does not provide any mechanism for ensuring the _private attributes are not used outside the module; 
it is just a naming convention.)

Note that there is no explicit compute_ranks function, although you will internally want to use one.  
The ranks need to be available when page_rank is called, but shouldn't be recomputed each time.  
(Hint: you can invalidate the ranks whenever the graph is changed.)

The WebCorpus type should provide these operations:
"""

class WebCorpus:
    def __init__(self):
        """
        Initializes a new, empty WebCorpus.
        """
        self._index = {}
        self._graph = {}
        self._ranks = None

    def add_word_occurrence(self, url, keyword):
        """
        Adds an occurrence of word on url to the corpus.
        """       
        if url not in self._graph:
            self._graph[url] = []
         
        if keyword in self._index:
            self._index[keyword].append(url)
        else:
            self._index[keyword] = [url]


    def add_link(self, source, sink):
        """
        If source is not a node in the corpus, adds source as a new node.
        If sink is not a node in the corpus, adds sink as a new node.
        Adds a link from source to sink to the corpus.
        """        
        if source not in self._graph:
            self._graph[source] = [sink]
        else:
            self._graph[source].append(sink)
        self._ranks = None # invalidate ranks after each graph modification    


    def _compute_ranks(self, d = 0.8, numloops = 10):
        """compute page ranks for the input web index.  d is the damping factor."""
        self._ranks = {}
            
        npages = len(self._graph)
        for url in self._graph:
            self._ranks[url] = 1.0 / npages
    
        for i in range(0, numloops):
            newranks = {}
            for page in self._graph:
                newrank = (1 - d) / npages
                for node in self._graph:
                    if page in self._graph[node]:
                        newrank = newrank + d * (self._ranks[node] / len(self._graph[node]))
                newranks[page] = newrank
            self._ranks = newranks
            

    def lookup(self, keyword):
        """
        Returns a list of urls where keyword appears in the corpus.  (If the
        keyword does not appear, returns an empty list.)  The listed urls may
        be in any order.
        """        
        if keyword in self._index:
            return self._index[keyword]
        else:
            return None


    def page_rank(self, url):
        """
        Returns the rank of the page url.
        """
        if not self._ranks:
            self._compute_ranks()
        if url not in self._ranks:
            return 0.0
        return self._ranks[url]
