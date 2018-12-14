import itertools as it
import numpy as np
import tensorflow as tf
import keras
import string
from models.Neural_helper import loss_smape

translator = str.maketrans(string.punctuation, ' '*len(string.punctuation)) 

class NeuralNetwork:
  def __init__(self, data, n_train, batch_size=256):
    self.batch_size=256
    self.data = data
    try:
      self.i_body = data.features.index('body')
    except ValueError:
      raise ValueError('please include body')

    self.tokenizer = keras.preprocessing.text.Tokenizer()
    comments = it.islice((f[self.i_body] for (_, _, f) in self.data.get_pairs()), 0, n_train)
    self.tokenizer.fit_on_texts(comments)

    self.create_model()

    # the plan, kinda:
    # train_batch(map(f,['hello my comment is derp', 'comment 2 is cool']),
    # scoresvec) where

    # f: lambda sent: to_categorical(one_hot(sent), num_classes = ???? something from
    # the other thing???)

    self.batches = self.get_batches(batch_size)
    for comments, scores in it.islice(self.batches, 0, n_train // batch_size): 
      # numpy??????
      print(comments.shape)
      self.model.train_on_batch(comments, scores)

  def create_model(self):
    self.model = keras.Sequential()
    n = len(self.tokenizer.word_counts)
    hidden_size = 256
    # in shape: (batch, input_length)
    self.model.add(keras.layers.Embedding(n+1, hidden_size, input_length=1))
    # (None, input_length, hidden_size)
    self.model.add(keras.layers.LSTM(hidden_size))
    # (None, hidden_size)
    self.model.add(keras.layers.TimeDistributed(keras.layers.Dense(1)))
    self.model.compile(loss=loss_smape, optimizer='adam', metrics=[loss_smape])

  def test(self, data, n_test):
    for comments, scores in it.islice(self.batches, 0, n_test // self.batch_size): 
      (self.model.evaluate(comments, scores))

  def sentence_to_one_hot(self, sentence):
      return [self.word_to_one_hot(word) for word in sentence.split()]

  def word_to_one_hot(self, word):
    n = len(self.tokenizer.word_counts)
    if word in self.tokenizer.word_counts:
        return keras.utils.to_categorical(keras.preprocessing.text.one_hot(word, n)) + np.array([0])
    else:
        return np.zeros(n) + np.array([1])


  def get_batches(self, batch_size):
    start = 0
    while True:
      #comments = it.islice((self.sentence_to_one_hot(f[self.i_body]) for (_, _, f) in self.data.get_pairs()), start, start + batch_size)
      comments, scores = it.tee(it.islice(self.data.get_pairs(), 0, batch_size))
      comments = np.array(list((self.sentence_to_one_hot(f[self.i_body]) for (_, _, f) in comments)))
      scores = np.array(list((s for (_, s, _) in scores)))
      start += batch_size
      yield (comments, scores)
