# import tensorflow as tf

# # Charger le jeu de données MNIST
# (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

# # Prétraitement des données
# x_train = x_train / 255.0
# x_test = x_test / 255.0

# # Construction du modèle
# model = tf.keras.Sequential([
#     tf.keras.layers.Flatten(input_shape=(28, 28)),
#     tf.keras.layers.Dense(128, activation='relu'),
#     tf.keras.layers.Dense(10, activation='softmax')
# ])

# # Compilation et entraînement du modèle
# model.compile(optimizer='adam',
#               loss='sparse_categorical_crossentropy',
#               metrics=['accuracy'])
# model.fit(x_train, y_train, epochs=5)

# # Sauvegarde du modèle
# model.save('mnist_model.h5')

import numpy as np
import pandas as pd

from sklearn.datasets import fetch_openml
from sklearn import metrics

train = pd.read_csv('static/data/train.csv')
test = pd.read_csv('static/data/test.csv')

