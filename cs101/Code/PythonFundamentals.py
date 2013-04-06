## Python Fundamentals
## https://www.udacity.com/wiki/cs253/Bridge_CS101


# Tuples
def tuple_test(x, y):
    x += 1
    y += 1
    return x, y

def foo(*args, **kwargs):
    return args if args else kwargs
    
    
# print (**foo(x=1, y=2))
print tuple_test(**foo(x=1, y=2))
print tuple_test(*tuple_test(1,2))