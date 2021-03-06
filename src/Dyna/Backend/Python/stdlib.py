import re, os
from term import Term, Cons, Nil, MapsTo
from collections import Counter
from utils import true, false, null, isbool
from math import log, exp, sqrt
from random import random as _random
from glob import glob


#def add(self, x):
#    if islist(x):
#        n = len(self.aslist)
#        m = len(x.aslist)
#        if n != m:
#            raise ValueError("Can't add list of unequal lengths (%s and %s)" % (len(self.aslist), len(x.aslist)))
#        else:
#            return todyna([a+b for a,b in zip(self.aslist, x.aslist)])
#    else:
#        # try to add scalar
#        return todyna([x+a for a in self.aslist])


def lookup(k, alist):
    a = dict(alist)
    return a.get(k)

def or_(x, y):
    if not (isbool(x) and isbool(y)):
        raise TypeError('`|` expected Boolean arguments, got `%s` and `%s`' \
                            % (type(x).__name__, type(y).__name__))
    return todyna(x or y)

def and_(x, y):
    if not (isbool(x) and isbool(y)):
        raise TypeError('`&` expected Boolean arguments, got `%s` and `%s`' \
                            % (type(x).__name__, type(y).__name__))
    return todyna(x and y)

def not_(x):
    if not isbool(x):
        raise TypeError('`!` expected Boolean arguments, got `%s`' \
                            % type(x).__name__)
    if x:
        return false
    else:
        return true

def gt(x, y):
    return todyna(x > y)

def gte(x, y):
    return todyna(x >= y)

def lt(x, y):
    return todyna(x < y)

def lte(x, y):
    return todyna(x <= y)

def eq(x,y):
    """
    My work around for discrepency in bool equality True==1 and False==0.
    >>> eq(true, 1)
    false
    >>> eq(1, 1.0)
    true
    """
    return todyna(x == y)

def not_eq(x, y):
    return todyna(x != y)

_range = range
def range(*x):
    return todyna(_range(*x))

def split(s, delim='\s+'):
    return todyna(re.split(delim, s))

def crash():
    class Crasher(Exception): pass
    raise Crasher('Hey, you asked for it!')

def pycall(name, *args):
    """
    Temporary foreign function interface - call Python functions from dyna!
    """
    args = tuple(topython(x) for x in args)
    x = eval(name)(*args)
    return todyna(x)

# TODO: should convert Term arguments
def topython(x):
    if islist(x):
        return [topython(y) for y in x.aslist]
    elif isinstance(x, MapsTo):
        return tuple(x.args)
#    elif isinstance(x, Term):
#        z = Term(x.fn, tuple(topython(y) for y in x.args))
#        z.value = topython(x.value)
#        return z
    else:
        return x

def todyna(x):
    if isinstance(x, (set, Counter)):
        x = list(x)
        x.sort()
        return todyna(x)
    elif x is True:
        return true
    elif x is False:
        return false
    elif isinstance(x, dict):
        return todyna([MapsTo(todyna(k), todyna(v)) for k,v in x.items()])
    elif isinstance(x, (list, tuple)):
        c = Nil
        for y in reversed(x):
            c = Cons(todyna(y), c)
        return c
    else:
        return x

#def get(x, i):
#    return x[i]

#def getkey(m, k):
#    return m[k]

#def setkey(m, k, v):
#    m[k] = v
#    return m

def islist(x):
    return isinstance(x, Cons) or x is Nil

def iter_cons(x):
    if not islist(x):
        raise TypeError("Attempting to iterate something which isn't a list. %r" % (x,))
    return x.like_chart()

def in_list(x, a):
    if not islist(a):
        raise TypeError("Attempting to iterate something which isn't a list. %r" % (a,))
    return todyna(x in a.aslist)

# should probably be done with memoized backchaining...
def read_lines(filename):
    with file(filename) as f:
        return f.readlines()

def uniform(a=0, b=1):
    return _random() * (b - a) + a
