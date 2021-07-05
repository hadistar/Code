# From https://www.tensorflow.org/get_started/get_started

import numpy as np

#---------------------1. Data generation------------------------------
num_points = 1000
vectors_set = []
for i in range(num_points):
         x1= np.random.normal(0.0, 0.55) #num 파이에서 정규분포 평균 0 v(x)이 0.55인 x1을 뽑아라.
         y1= x1 * 0.1 + 0.3 + np.random.normal(0.0, 0.03) #wright 0.1 bias 0.3
         vectors_set.append([x1, y1]) #vertors set shape 은 어떤 형태? np.shape(vectors_set)
         # vector_set[0] // 두번 돌지...

x_data = [v[0] for v in vectors_set] #for문이 천번 돌면서 x1 y1 생성. 1행부터 1000행까지 v(0) the first component.
y_data = [v[1] for v in vectors_set]

#----------------------2. plot ---------------------------------------

import matplotlib.pyplot as plt

plt.figure(1)
plt.plot(x_data, y_data, 'ro', label='Original data')
plt.legend()
plt.show()
#plt.line()
#---------------------3. Tensorflow ---------------------------------

import tensorflow as tf

# Define layer
layer0 = tf.keras.layers.Dense(units=1, input_shape=[1]) #레이어를 만들껀데 unit이 1 한층짜리 1

model = tf.keras.Sequential([layer0]) #모델은 sequential 이다 연결이 되어있고...

# Compile model
model.compile(loss='mean_squared_error',
              optimizer=tf.keras.optimizers.Adam(1))

# Train the model
history = model.fit(x_data, y_data, epochs=100, verbose=False)

# Prediction
print('Prediction: {}'.format(model.predict([1])))

# Get weight and bias
weights = layer0.get_weights()
print('weight: {} bias: {}'.format(weights[0], weights[1]))

plt.figure(2)
plt.xlabel('Epoch Number')
plt.ylabel("Loss Magnitude")
plt.plot(history.history['loss'])
plt.show()

plt.figure(3)
plt.plot(x_data, y_data, 'ro', label='Original data')
plt.plot(x_data, model.predict(x_data), 'k-', label = "Predicted")
plt.legend()
plt.show()