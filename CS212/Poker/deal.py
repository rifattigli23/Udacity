import random 

def deal(numhands, n=5, deck=[t+s for r in '23456789TJQKA' for s in 'SHDC']):
  "Shuffle the deck and deal out numhands n-card hands."
  random.shuffle(deck)
  return [deck[n*i:n*(i+1)] for i in range(numhands)]