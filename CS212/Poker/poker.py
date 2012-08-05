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
  correctStraight = range(min(ranks),max(ranks)+1)
  correctStraight.sort(reverse=True)
  return ranks == correctStraight

def flush(hand):
  "Return True if all the cards have the same suit."
  suits = [suit for value,suit in hand]
  return [suit==suits[0] for value,suit in hand].count(True) == 5  

def test():
  "Test cases for the functions in poker program."
  sf = "6C 7C 8C 9C TC".split()
  fk = "9D 9H 9S 9C 7D".split()
  fh = "TD TC TH 7C 7D".split()
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

