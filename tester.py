#!/usr/bin/env python3
from models.data import Data
from models.Logistic import Logistic as Model
from models.eval import smape
import matplotlib.pyplot as plt

offset = 0
n_train = 1000
n_test = 100

data = Data('data/database.sqlite')
data.read('May2015', ['body'], offset=offset)
model = Model(data, n_train)
predicted, actual = model.test(data, n_test)
print('Smape: {}'.format(smape(predicted, actual)))

plt.plot(predicted, actual, 'o')
plt.ylim(top=40)
plt.show()
