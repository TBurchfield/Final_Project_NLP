import sqlite3

class Data:
  def __init__(self, filename):
    self.filename = filename

  def read(self, tablename, features, offset=0):
    self.offset = offset
    self.n_features = len(features)
    self.features = features
    db = sqlite3.connect('file:{}?mode=ro'.format(self.filename), uri=True)
    c = db.cursor()
    self.pairs = c.execute("SELECT {} from {}".format(', '.join(['score'] + features), tablename))

  def get_pairs(self):
    for i, (score, *features) in enumerate(self.pairs):
      if i >= self.offset:
        yield i, score, features
