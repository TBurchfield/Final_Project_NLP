#!/usr/bin/env python3

from collections import defaultdict

import json
import string
import sqlite3


translator = str.maketrans('', '', string.punctuation)
n_train = 1000
n_test = 100


class BaselineModel:
  def __init__(self):
    self.counts = defaultdict(float)
    self.word_instances = defaultdict(int)
    self.avg_score = 0
    self.avg_word = None

  def avg_word_score(self):
      if self.avg_word:
          return self.avg_word

      self.avg_word = sum((self.counts[w] / self.word_instances[w] for w in self.counts))/ len(self.word_instances)
      return self.avg_word


def process_pairs(pairs):
    for i, (body, score) in enumerate(pairs):
        processed = body.translate(translator).lower().split()
        yield i, set(processed), score


def train(pairs):
  #return model
  model = BaselineModel()
  total_scores = 0
  for i, body, score in process_pairs(pairs):

    total_scores += score
    n = len(body)
    for word in body:
      model.counts[word] += score / n
      model.word_instances[word] += 1

    if i >= n_train - 1:
      break

  model.avg_score = total_scores / n_train
  return model


def metric(x, y):
  denom = abs(x) + abs(y)
  return abs(x - y) / denom if denom > 0 else 0


def test(model, pairs):
  # returns (score, bad_score)
  # because we have five fingers
  differences = 0
  bad_differences = 0

  for i, body, upvotes in process_pairs(pairs):
    guess = 0

    n = len(body)
    for word in body:
      # Otherwise long comments will be favored
      if model.word_instances[word] != 0:
        guess += model.counts[word] / model.word_instances[word]
      else:
        guess += model.avg_word_score()

    differences += metric(guess, upvotes)
    bad_differences += metric(model.avg_score, upvotes)

    if i >= n_test - 1:
      break

  return (differences / n_test, bad_differences / n_test)


def get_db_cursor():
    db = sqlite3.connect('file:../data/database.sqlite?mode=ro', uri=True)
    c = db.cursor()
    return c


def get_schema(cursor):
  for r in cursor.execute("pragma table_info({})".format(table)):
    print(r)


if __name__ == '__main__':
    c = get_db_cursor()
    table = "May2015"
    pairs = c.execute("SELECT body, score from {}".format(table))
    model = train(pairs)
    score, bad_score = test(model, pairs)
    print('score: {}'.format(score))
    print('if we had just guessed the average score of {}: {}'.format(model.avg_score, bad_score))
