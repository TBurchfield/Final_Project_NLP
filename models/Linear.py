from sklearn.feature_extraction.text import CountVectorizer as Vectorizer
from sklearn.linear_model import LinearRegression
import numpy as np
import itertools as it

class Linear:
  def __init__(self, data, n_train):
    try:
      self.i_body = data.features.index('body')
    except ValueError:
      raise ValueError('pls Don"t do that i need body')
    comments, scores = it.tee(it.islice(data.get_pairs(), 0, n_train))
    comments = np.array(list(f[self.i_body] for (i, s, f) in comments))
    scores = np.array(list(s for (i, s, f) in scores))
    self.vectorizer = Vectorizer(ngram_range=(1,2))
    X = self.vectorizer.fit_transform(comments)
    self.model = LinearRegression(normalize=True).fit(X, scores)

  def test(self, data, n_test):
    comments, scores = it.tee(it.islice(data.get_pairs(), 0, n_test))
    comments = np.array(list(f[self.i_body] for (i, s, f) in comments))
    scores = np.array(list((s for (i, s, f) in scores)))
    X = self.vectorizer.transform(comments)
    predict = self.model.predict(X)
    print(self.vectorizer.stop_words_)
    '''
    for c, p, s in zip(comments, predict, scores):
      if p < -140:
        C = np.array([c])
        Cx = self.vectorizer.transform(C)
        inv = self.vectorizer.inverse_transform(Cx)[0]
        scorepairs = []
        me = Cx.toarray()[0]
        sub = self.model.predict(np.array([[0] * len(me)]))[0]
        for i, n in enumerate(me):
          w_vec = np.array([([0] * i) + [n] + ([0]*(len(me)-(i+1)))])
          w_result = self.model.predict(w_vec)[0] - sub
          w = self.vectorizer.inverse_transform(w_vec)[0]
          if not len(w):
            continue
          w = w[0]
          scorepairs.append((w_result, n, w))
        sinv = sorted(scorepairs)
        s = sum([r for r, _, _ in scorepairs]) + sub
        print(sinv)
        print(s)
    '''
    return (predict, scores)
