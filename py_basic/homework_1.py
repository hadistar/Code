# import package
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

# load sample
xy = np.loadtxt('data-04-zoo.csv', delimiter=',', dtype=np.float32)
x_data = xy[:, 0:-1]
y_data = xy[:, [-1]]

# shape of data
print(x_data.shape, y_data.shape)


nb_classes = 7

# Convert y_data to one_hot
y_one_hot = tf.keras.utils.to_categorical(y_data, nb_classes)
print("one_hot:", y_one_hot)

# partition data into train/test sets
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x_data, y_one_hot, test_size=0.2, shuffle=True)

print(x_train.shape)
print(x_test.shape)
print(y_train.shape)
print(y_test.shape)

tf.model = tf.keras.Sequential()
tf.model.add(tf.keras.layers.Dense(units=nb_classes, input_dim=16, activation='softmax'))
tf.model.compile(loss='categorical_crossentropy', optimizer=tf.keras.optimizers.SGD(lr=0.1), metrics=['accuracy'])
tf.model.summary()
history = tf.model.fit(x_test, y_test, batch_size=50, epochs=1000)

plt.plot(history.history['accuracy'])
plt.legend(['training'], loc = 'upper left')
plt.show()


result= tf.model.evaluate(x_test,y_test)
print('Test accuracy: ', result[1])


test_data = np.array([[0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0]])
print(tf.model.predict(test_data), tf.model.predict_classes(test_data))


# 숫자형 -> 문자형
# 1
import pandas as pd
df = pd.DataFrame({'숫자특성':[0,1,2,3,4,5,6],'factor형 특성':['dog','lion','tiger','cat','horse','mouse','rabbit']})
print('df\n{}'.format(df))
print(df.loc[df["숫자특성"]==tf.model.predict_classes(test_data)[0], ["factor형 특성"]])

# 2
text = {0:'dog',1:'lion',2:'tiger',3:'cat',4:'horse',5:'mouse',6:'rabbit'}
Print(df(test_data))

tf.model.predict_classes(test_data)[0]
text[tf.model.predict_classes(test_data)[0]]