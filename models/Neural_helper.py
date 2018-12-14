import keras.backend as K
def loss_smape(y_true, y_pred):
  return K.sum(K.abs(y_true - y_true) / (K.abs(y_true) + K.abs(y_pred)))
