# Lab 2 Linear Regression
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

# X and Y data
x_train = [1, 2, 3]
y_train = [2, 4, 6]

# Try to find values for W and b to compute y_data = x_data * W + b
# We know that W should be 1 and b should be 0

x_train = np.array(x_train)
y_train = np.array(y_train)

line_fitter = LinearRegression() // 변수선언 이름 아무거나 해도 되는거야?

line_fitter.fit(x_train.reshape(-1,1), y_train) // x는 vertor 형태로 되어있어야 한다.

# 주의사항: X는 vector 형태로 되어있어야 함 (reshape의 이유)

print ("W=",line_fitter.coef_)
print ("b=",line_fitter.intercept_)
print (line_fitter.predict([[4],[5]]))

plt.figure()
plt.scatter(x_train,y_train, color='red', label='observed')
plt.plot(x_train, line_fitter.predict(x_train.reshape(-1,1)), 'k-', label="predicted")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.show()