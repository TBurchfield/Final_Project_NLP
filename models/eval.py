import numpy as np

def smape(guessed, actual):
  def safesmape(g, a):
    denom = abs(g) + abs(a)
    return abs(g-a) / denom if denom > 0 else 0
  return sum(safesmape(g, a) for g, a in zip(guessed, actual)) / len(guessed)
