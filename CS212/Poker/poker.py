def poker(hands):
  "Return the best hand: poker([hand,...]) => hand"
  return max(hands, key=hand_rank)

def hand_rank(hand):
  return None # we wil be changing this later
