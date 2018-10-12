#!/usr/bin/env python3

from collections import defaultdict
import string
import sqlite3
import json

translator = str.maketrans('', '', string.punctuation)
n_train = 1000
n_test = 100
class Model:
  def __init__(self):
    self.counts = defaultdict(float)
    self.avg_score = 0

def train(pairs):
  #return model
  model = Model()
  all_scores = 0
  for i, (body, score) in enumerate(pairs):
    processed = body.translate(translator).lower().split()
    n = len(processed)
    all_scores += score
    for word in processed:
      # Otherwise long comments will be favored
      model.counts[word] += score / n
    if i >= n_train:
      break
  avg = all_scores / n_train
  model.avg_score = avg
  return model

def test(model, pairs):
  # returns (score, bad_score)
  # because we have five fingers
  differences = 0
  bad_differences = 0
  for i, (body, upvotes) in enumerate(pairs):
    guess = 0
    processed = body.translate(translator).lower().split()
    n = len(processed)
    for word in processed:
      # Otherwise long comments will be favored
      guess += model.counts[word] / n
    denom = abs(guess) + abs(upvotes)
    bad_denom = abs(model.avg_score) + abs(upvotes)
    difference = abs(guess - upvotes) / denom if denom > 0 else 0
    bad_difference = abs(model.avg_score - upvotes) / bad_denom if bad_denom > 0 else 0
    differences += difference
    bad_differences += bad_difference
    if i >= n_test:
      break
  score = differences / n_test
  bad_score = bad_differences / n_test
  return (score, bad_score)

def get_schema(cursor):
  for r in cursor.execute("pragma table_info({})".format(table)):
    print(r)

if __name__ == '__main__':
    db = sqlite3.connect('file:../data/database.sqlite?mode=ro', uri=True)
    c = db.cursor()
    table = "May2015"
    pairs = c.execute("SELECT body, score from {}".format(table))
    model = train(pairs)
    score, bad_score = test(model, pairs)
    print('score: {}'.format(score))
    print('if we had just guessed the average score of {}: {}'.format(model.avg_score, bad_score))
