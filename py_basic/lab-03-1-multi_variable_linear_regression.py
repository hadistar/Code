# Lab 4 Multi-variable linear regression
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

x1_data = [73., 93., 89., 96., 73., 40., 50., 60., 70., 80.]
x2_data = [80., 88., 91., 98., 66., 70., 80., 90., 70., 100.]
x3_data = [75., 93., 90., 100., 70., 70., 80., 60., 70., 90.]

y_data = [152., 185., 180., 196., 142., 150., 170., 190., 160., 180.]

x1_data = np.array(x1_data)
x2_data = np.array(x2_data)
x3_data = np.array(x3_data)

x = np.hstack((x1_data.reshape(-1,1), x2_data.reshape(-1,1), x3_data.reshape(-1,1))) #열합치기
y = np.array(y_data)

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8, test_size=0.2) #test가 낮은 경우, 데이터의 수가 확보가 되지않아 reasonable 하지 않은 것.

mlr = LinearRegression()
mlr.fit(x_train, y_train)

# y = a*x1 + b*x2 + c*x3 + d

print("a,b,c=", mlr.coef_)
print("d=",mlr.intercept_)
print("tran accuracy=",mlr.score(x_train,y_train))

y_predict = mlr.predict(x_test)

plt.figure(1)
plt.plot(y_test, y_predict, 'ro')

plt.xlabel("Observed")
plt.ylabel("Predicted")
plt.show()


y_predict = mlr.predict(x_train) # mlr.predict 는 그 자체로서의 함수 => predict는 새로운 값을 넣을떄 들어가는 함수
line_fitter = LinearRegression()
line_fitter.fit(y_train.reshape(-1,1), y_predict)

plt.figure(2)
plt.plot(y_train, mlr.predict(x_train), 'bo')
plt.plot(y_train, line_fitter.predict(y_train.reshape(-1,1)), 'k-')
plt.xlabel("Observed")
plt.ylabel("Predicted")
plt.show()
