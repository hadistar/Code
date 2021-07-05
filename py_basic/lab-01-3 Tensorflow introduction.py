
# Machine learning introduction
# https://www.youtube.com/watch?v=qPMeuL2LIqY&list=PLlMkM4tgfjnLSOjrEJN31gZATbcj_MpUm&index=2

# Tensor flow intorduction
# https://www.youtube.com/watch?v=mviPXahg8SA
# http://datahacker.rs/tensorflow-constants-and-variables/

# Ranking
# https://www.kdnuggets.com/2018/09/deep-learning-framework-power-scores-2018.html

import tensorflow as tf
import numpy as np

print (tf.multiply(3,2))

# Initialize two constants
x1 = tf.constant([1,2,3,4])
x2 = tf.constant([5,6,7,8])

# add
result = tf.add(x1, x2)

# Print the result
print(result)

a = [[1,2],[3,4]]
b = [[1,0],[0,1]]

c = np.array(a)
d = np.array(b)

print (tf.multiply(a,b))
print (tf.linalg.matmul(a,b))

print (tf.multiply(c,d))
print (tf.linalg.matmul(c,d))