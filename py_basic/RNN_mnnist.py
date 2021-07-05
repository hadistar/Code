import numpy as np
import tensorflow as tf
import pandas as pd
from tensorflow.keras.utils import plot_model

# Load data
mnist_train = pd.read_csv("train.csv")
mnist_test = pd.read_csv("test.csv")
print(mnist_train)
print(mnist_test)

#라벨 버리기 긔긔
x_train = mnist_train.drop(labels = "label", axis = 1)
print(x_train)
y_train = mnist_train["label"]
print(y_train)

#nomalization
x_train = x_train/255.0
mnist_test = mnist_test/255.0

print(x_train.shape)
print(y_train.shape)
print(mnist_test.shape)

x_train = x_train.values.reshape(-1, 28, 28, 1)
mnist_test = mnist_test.values.reshape(-1, 28, 28, 1)
print(x_train.shape)

# hyper parameters
learning_rate = 0.001
training_epochs = 20
batch_size = 1000

# one hot encode y data
nb_classes = 10
y_train = tf.keras.utils.to_categorical(y_train, nb_classes)
print(y_train[3])

# L1
input_layer = tf.keras.layers.Input(shape = (28, 28, 1))
hidden_layer_1 = tf.keras.layers.Conv2D(32, kernel_size=(3, 3), activation='relu')(input_layer)
norm_1 = tf.keras.layers.BatchNormalization()(hidden_layer_1)
max_1 = tf.keras.layers.MaxPooling2D(pool_size=(2, 2), strides=(2,2))(norm_1)
dropout_layer_1 = tf.keras.layers.Dropout(0.25)(max_1)

# L2
hidden_layer_2 = tf.keras.layers.Conv2D(64, kernel_size=(3, 3), activation='relu')(dropout_layer_1)
norm_2 = tf.keras.layers.BatchNormalization()(hidden_layer_2)
max_2 = tf.keras.layers.MaxPooling2D(pool_size=(2, 2), strides=(2,2))(norm_2)
flatten_layer = tf.keras.layers.Flatten()(max_2)
dropout_layer_2 = tf.keras.layers.Dropout(0.25)(flatten_layer)

# L3 fully connected
hidden_layer_3 = tf.keras.layers.Dense(256, activation=tf.keras.activations.relu)(dropout_layer_2)
hidden_layer_4 = tf.keras.layers.Dense(128, activation=tf.keras.activations.relu)(hidden_layer_3)
dropout_layer_3 = tf.keras.layers.Dropout(0.5)(hidden_layer_4)
output_layer = tf.keras.layers.Dense(10, kernel_initializer='glorot_normal', activation='sigmoid')(dropout_layer_3)

# fit
model = tf.keras.Model(inputs = input_layer, outputs = output_layer)
model.compile(loss='categorical_crossentropy', optimizer=tf.keras.optimizers.Adam(lr=learning_rate), metrics=['accuracy'])
model.fit(x_train, y_train, batch_size=batch_size, epochs=training_epochs)
model.summary()

#tf.keras.utils.plot_model(model, "digit_classifier_model.png", show_shapes=True)

# predict results
results = model.predict(mnist_test)
results = np.argmax(results, axis=1)
results = pd.Series(results, name="Label")

# export to csv
submission = pd.concat([pd.Series(range(mnist_test.shape), name="ImageId"), results], axis=1)
submission.to_csv("mnist_result.csv", index=False)

