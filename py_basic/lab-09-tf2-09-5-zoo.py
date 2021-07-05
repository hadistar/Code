# Lab 9 - DNN Classifier
import tensorflow as tf
import numpy as np
# Define the Keras TensorBoard callback.

from datetime import datetime
# for tensorboard
logdir="logs/" + datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=logdir)

# Predicting animal type based on various features
xy = np.loadtxt('data-04-zoo.csv', delimiter=',', dtype=np.float32)
x_data = xy[:, 0:-1]
y_data = xy[:, [-1]].flatten()

print(x_data.shape, y_data.shape)

'''
(101, 16) (101, 1)
'''

nb_classes = 7  # 0 ~ 6

# Convert y_data to one_hot
y_one_hot = tf.keras.utils.to_categorical(y_data, nb_classes)
print("one_hot:", y_one_hot)

tf.model = tf.keras.Sequential()
tf.model.add(tf.keras.layers.Dense(units=16, input_dim=16, activation='sigmoid'))
tf.model.add(tf.keras.layers.Dense(units=16, activation='sigmoid'))
tf.model.add(tf.keras.layers.Dense(units=16, activation='sigmoid'))
tf.model.add(tf.keras.layers.Dense(units=nb_classes, activation='softmax'))

tf.model.compile(loss='categorical_crossentropy', optimizer=tf.keras.optimizers.SGD(lr=0.1), metrics=['accuracy'])
tf.model.summary()

history = tf.model.fit(x_data, y_one_hot, epochs=3000, callbacks=[tensorboard_callback])
# callbacks: for tensorboard

# Single data test
test_data = np.array([[0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0]]) # expected prediction == 3 (feathers)
print(tf.model.predict(test_data), np.argmax(tf.model.predict(test_data)))

# Full x_data test
pred = tf.model.predict_classes(x_data)
for p, y in zip(pred, y_data.flatten()):
    print("[{}] Prediction: {} True Y: {}".format(p == int(y), p, int(y)))

# python -m tensorboard.main --logdir="logs/20201214-180514" --port=6006

# print epochs by 500?