from sklearn.feature_extraction.text import CountVectorizer as Vectorizer
from sklearn.linear_model import LogisticRegression
import numpy as np
import itertools as it

class Logistic:
  def __init__(self, data, n_train):
    try:
      self.i_body = data.features.index('body')
    except ValueError:
      raise ValueError('please include body')

    comments, scores = it.tee(it.islice(data.get_pairs(), 0, n_train))
    comments = np.array(list(f[self.i_body] for (i, s, f) in comments))
    scores = np.array(list((s for (i, s, f) in scores)))
    self.vectorizer = Vectorizer()
    X = self.vectorizer.fit_transform(comments)
    self.model = LogisticRegression(solver='lbfgs').fit(X, scores)

  def test(self, data, n_test):
    comments, scores = it.tee(it.islice(data.get_pairs(), 0, n_test))
    comments = np.array(list(f[self.i_body] for (i, s, f) in comments))
    scores = np.array(list((s for (i, s, f) in scores)))
    X = self.vectorizer.transform(comments)
    predict = self.model.predict(X)
    return (predict, scores)
