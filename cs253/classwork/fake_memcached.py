
# QUIZ implement the basic memcache functions

CACHE = {}

#return True after setting the data
def set(key, value):
    ###Your set code here.
    CACHE[key] = value
    if CACHE[key]:
        return True
    else: 
        return False

#return the value for key
def get(key):
    ###Your get code here.
    return CACHE.get(key, None)

#delete key from the cache
def delete(key):
    ###Your delete code here.
    CACHE.pop(key)

#clear the entire cache
def flush():
    ###Your flush code here.
    CACHE.clear()

print set('x', 1)
#>>> True

print get('x')
#>>> 1

print get('y')
#>>> None

delete('x')
print get('x')
#>>> None

print set('x', 1)
#>>> True

print get('x')
#>>> 1

flush()
print get('x')
#>>> None
