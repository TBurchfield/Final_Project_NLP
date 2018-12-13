#!/usr/bin/env python3
from models.data import Data
from models.NeuralNetwork import NeuralNetwork as Model
from models.eval import smape
import matplotlib.pyplot as plt
import numpy as np

offset = 0
n_train = 10000
n_test = 500

data = Data('data/database.sqlite')
data.read('May2015', ['body'], offset=offset)
model = Model(data, n_train)
print('fuck you')
predicted, actual = model.test(data, n_test)
print('fuck you v2')
print('Smape: {}'.format(smape(predicted, actual)))
print('fuck you v3')
print(n_train)
print(n_test)
#l = np.array(["", "the", "reddit", "a", "dog"])
#testX = model.vectorizer.transform(l)
#p = model.model.predict(testX)
#print(model.model.intercept_)
#print(p)
#print(l)


#plt.plot(predicted, actual, 'o')
#plt.ylim()
#plt.show()
