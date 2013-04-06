import itertools

def imright(h1, h2):
  return h1-h2 == -1

def nextto(h1, h2):
  return abs(h1-h2) == 1

def zebra_puzzle():
  "Return a tuple (WATER, ZEBRA) indicating their house numbers."
  houses = first, _, middle, _, _ = [1, 2, 3, 4, 5]
  orderings = list(itertools.permutations(houses)) #1
  return next((WATER, ZEBRA)
          for (red, green, ivory, yellow, blue) in orderings
          
          for (Englishman, Spaniard, Ukranian, Japanese, Norwegian) in orderings
          if Englishman is red            #2
          if imright(green, ivory)        #6
          if Norwegian is first           #10
          if nextto(Norwegian, blue)       #15
   
          for (dog, snails, fox, horse, ZEBRA) in orderings
          if Spaniard is dog              #3

          for (coffee, tea, milk, oj, WATER) in orderings
          if coffee is green              #4
          if Ukranian is tea              #5
          if milk is middle               #9
          
          for (OldGold, Kools, Chesterfields, LuckyStrike, Parliaments) in orderings
          if OldGold is snails            #7
          if Kools is yellow               #8
          if nextto(Chesterfields, fox)   #11
          if nextto(Kools, horse)         #12
          if LuckyStrike is oj            #13
          if Japanese is Parliaments      #14
          )

import time

def timedcall(fn, *args):
    "Call function with args; return the time in seconds and result."
    t0 = time.clock()
    result = fn(*args)
    t1 = time.clock()
    return t1-t0, result

def average(numbers):
    "Return the average (arithmetic mean) of a sequence of numbers."
    return sum(numbers) / float(len(numbers)) 

def timedcalls(n, fn, *args):
    """Call fn(*args) repeatedly: n times if n is an int, or up to
    n seconds if n is a float; return the min, avg, and max time"""
    # Your code here.
    if isinstance(n, int):
      times = [timedcall(fn, *args)[0] for _ in range(n)]
    else:
      times = []
      while sum(times) < n:
        times.append(timedcall(fn, *args)[0])
    return min(times), average(times), max(times)

print timedcalls(10.0, zebra_puzzle, )