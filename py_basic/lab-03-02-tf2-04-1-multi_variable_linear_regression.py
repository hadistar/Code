# Lab 4 Multi-variable linear regression
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

x_data = [[73., 80., 75.],
          [93., 88., 93.],
          [89., 91., 90.],
          [96., 98., 100.],
          [73., 66., 70.]]
y_data = [[152.],
          [185.],
          [180.],
          [196.],
          [142.]]

tf.model = tf.keras.Sequential() #keras.sequentail 이라는 도화지를 편다는 개념?

tf.model.add(tf.keras.layers.Dense(units=1, input_dim=3))  # input_dim=3 gives multi-variable regression
#레이어 하나에 인풋 디멘젼을 3으로 주고 싶다. 자동으로 multi-variable regression으로 주는거야.
tf.model.add(tf.keras.layers.Activation('linear'))  # this line can be omitted, as linear activation is default
# advanced reading https://towardsdatascience.com/activation-functions-neural-networks-1cbd9f8d91d6

tf.model.compile(loss='mse', optimizer=tf.keras.optimizers.SGD(lr=1e-5)) #SGD 기울기 미분해서 음으로 가는거...1의 -5승씩 조정
tf.model.summary() #summary를 싱행해보면
history = tf.model.fit(x_data, y_data, epochs=500)

y_predict = tf.model.predict(x_data)
print(y_predict)

plt.figure(1)
plt.plot(y_data, y_predict, 'ro')

plt.xlabel("Observed")
plt.ylabel("Predicted")
plt.show()