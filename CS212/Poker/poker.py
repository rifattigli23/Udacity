def poker(hands):
  "Return the best hand: poker([hand,...]) => hand"
  return max(hands, key=hand_rank)

def hand_rank(hand):
  ranks = card_ranks(hand)
  if straight(ranks) and flush(hand):            # straight flush
    return (8, max(ranks))
  elif kind(4, ranks):                           # 4 of a kind
    return (7, kind(4, ranks), kind(1, ranks))
  elif kind(3, ranks) and kind(2, ranks):        # full house
    return (6, kind(3, ranks), kind(2, ranks))
  elif flush(hand):                              # flush
    return (5, ranks)
  elif straight(ranks):                          # straight
    return (4, max(ranks))
  elif kind(3, ranks):                           # 3 of a kind
    return (3, kind(3,ranks), ranks)
  elif two_pair(ranks):                          # 2 pair
    return (2, max(two_pair(ranks)), min(two_pair(ranks)), ranks)
  elif kind(2, ranks):                           # kind 
    return (1, kind(2, ranks), ranks)
  else:                                          # high card
    return (0, ranks)

def card_ranks(hand):
  "Return a list of the ranks, sorted with higher first"  
  ranks = ['--23456789TJQKA'.index(r) for r,s in hand]
  ranks.sort(reverse=True)
  return ranks

def straight(ranks):
  "Return True if the ordered ranks form a 5-card straight."
  return (max(ranks)-min(ranks) == 4) and len(set(ranks)) == 5

def flush(hand):
  "Return True if all the cards have the same suit."
  suits = [s for r,s in hand]
  return len(set(suits)) == 1

def kind(n, ranks):
  """Return the first rank that this hand has exactly n of.
  Return None if there is no n-of-a-kind in the hand."""
  for r in ranks:
    if ranks.count(r) == n:
      return r
  return None

def two_pair(ranks):
  """If there are two pair, return the two ranks as a
  tuple: (highest, lowest); otherwise return None."""
  highPair = kind(2, ranks)
  lowPair = kind(2, list(reversed(ranks)))
  if highPair and lowPair != highPair:
    return (highPair, lowPair)
  else:
    return None

def test():
  "Test cases for the functions in poker program."
  sf = "6C 7C 8C 9C TC".split() # straight flush
  fk = "9D 9H 9S 9C 7D".split() # four of a kind
  fh = "TD TC TH 7C 7D".split() # full house
  tp = "5S 5D 9H 9C 6S".split() # two pair
  s1 = "AS 2S 3S 4S 5C".split() # A-5 straight
  s2 = "2C 3C 4C 5S 6S".split() # 2-6 straight
  ah = "AS 2S 3S 4S 6S".split() # A high
  sh = "2S 3S 4S 6C 7D".split() # 7 high
  assert poker([s1, s2, ah, sh]) == s2
  fkranks = card_ranks(fk)
  tpranks = card_ranks(tp)
  assert kind(4, fkranks) == 9
  assert kind(3, fkranks) == None
  assert kind(2, fkranks) == None
  assert kind(1, fkranks) == 7
  assert two_pair(fkranks) == None
  assert two_pair(tpranks) == (9,5)
  assert straight([9, 8, 7, 6, 5]) == True
  assert straight([9, 8, 8, 6, 5]) == False
  assert flush(sf) == True
  assert flush(fk) == False
  assert card_ranks(sf) == [10, 9, 8, 7, 6]
  assert card_ranks(fk) == [9, 9, 9, 9, 7]
  assert card_ranks(fh) == [10, 10, 10, 7, 7]  
  assert poker([sf, fk, fh]) == sf
  assert poker([fk,fh]) == fk
  assert poker([fh, fh]) == fh
  assert poker([sf]) == sf
  assert poker([sh] + 99*[fh]) == sf 
  assert hand_rank(sf) == (8,10)
  assert hand_rank(fk) == (7,9,7)
  assert hand_rank(fh) == (6,10,7)  
  
  return "tests pass"

print test()

