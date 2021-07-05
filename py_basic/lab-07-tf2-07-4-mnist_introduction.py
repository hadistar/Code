# Lab 7 Learning rate and Evaluation
import tensorflow as tf
import matplotlib.pyplot as plt
import random

mnist = tf.keras.datasets.mnist

# Check out https://www.tensorflow.org/get_started/mnist/beginners for
# more information about the mnist dataset

nb_classes = 10

# MNIST data image of shape 28 * 28 = 784
# 0 - 9 digits recognition = 10 classes

(x_train, y_train), (x_test, y_test) = mnist.load_data() #x_train 흑백을 200

print (x_train.shape)
print (y_train.shape)
print (x_test.shape)
print (y_test.shape)

print (x_train[0].shape)
print (x_train[0])
print (y_train[0])


def show_data(arr):
    plt.imshow(arr, cmap=plt.cm.binary)

    reshape_data = arr.reshape(-1, )
    for index, data in enumerate(reshape_data):
        print('{:3d}'.format(data), end='')
        if index % 28 == 27:
            print()

show_data(x_train[0])

plt.imshow(x_train[0], cmap='Greys', interpolation='None')
plt.show()

#딥러닝은 특징을..리니어 리그레이션 기울기와 절편 -> feature(기울기)