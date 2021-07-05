# import package
import numpy as np

# load sample
xy = np.loadtxt('data-04-zoo.csv', delimiter=',', dtype=np.float32)
x_data = xy[:, 0:-1]
y_data = xy[:, [-1]]

# shape of data
print(x_data.shape, y_data.shape)

#import Gaussian Naive Bayes model
from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB

#Create a Gaussian calssifier
model = BernoulliNB()

#Train the model using the training sets
model.fit(x_data, y_data)

#predict Output
predicted = model.predict([[0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0]])
print("Predicted value:",predicted)

#numeric to character
import pandas as pd
df = pd.DataFrame({'숫자특성':[0,1,2,3,4,5,6],'factor형 특성':['dog','lion','tiger','cat','horse','mouse','rabbit']})
print('df\n{}'.format(df))
print(df.loc[df["숫자특성"]==predicted[0], ["factor형 특성"]])