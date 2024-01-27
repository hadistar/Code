import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Arial'



import seaborn as sns

df = pd.read_csv('D:\\OneDrive\\3.py_SCH\\data_OP_ML\\PM2.5_OP_2019-2021_2.csv')


# for Pearson coefficient heatmap figure

df_pearson = df[['OPv (DTTv)', '온도', '습도', '풍속', 'O3', 'NO2', 'CO', 'PM2.5', 'PM10',
       'OC', 'EC', 'TC', 'WSTN', 'WSIN', 'WSON', 'WSOC', 'Cl', 'NO3', 'SO4',
       'Na', 'NH4', 'K', 'Ca', 'Mg', 'acidity', 'Li', 'Al', 'Ti', 'V', 'Cr',
       'Mn', 'Fe', 'Ni', 'Cu', 'Zn', 'As', 'Cd', 'Pb', 'SO2']]

df_pearson.columns = ['OPv', 'Temperature', 'Humidity', 'Wind speed', 'O$_3$', 'NO$_2$', 'CO', 'PM$_{2.5}$', 'PM$_{10}$',
       'OC', 'EC', 'TC', 'WSTN', 'WSIN', 'WSON', 'WSOC', 'Cl', 'NO3', 'SO4',
       'Na', 'NH$_4^+$', 'K', 'Ca', 'Mg', 'Acidity', 'Li', 'Al', 'Ti', 'V', 'Cr',
       'Mn', 'Fe', 'Ni', 'Cu', 'Zn', 'As', 'Cd', 'Pb', 'SO$_2$']

corr = df_pearson.corr()

plt.figure(figsize=(16,12))
sns.set_theme(style="white")
heatmap = sns.heatmap(corr, cmap='coolwarm',vmin=-1.0, vmax=1.0)
plt.show()


# 1:1 plots

from sklearn.metrics import r2_score
from sklearn import linear_model
import sklearn

trainset = pd.read_csv('D:\\Github\\3.py_SCH\\result_DNN_trainset_w_yellow.csv')
testset = pd.read_csv('D:\\Github\\3.py_SCH\\result_DNN_testset_w_yellow.csv')

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 13
plt.rcParams.update({'figure.autolayout': True})

x = testset.iloc[:,0]
y = testset.iloc[:,1]

linreg = linear_model.LinearRegression()
# Fit the linear regression model
model = linreg.fit(np.array(x).reshape(-1,1), np.array(y).reshape(-1,1))

# Get the intercept and coefficients
intercept = model.intercept_
coef = model.coef_
result = [intercept, coef]
predicted_y = np.array(x).reshape(-1,1) * coef + intercept
r_squared = sklearn.metrics.r2_score(y, predicted_y)


plt.figure(figsize=(5, 5))
# plt.scatter(x, y, s=40, facecolors='none', edgecolors='k')
plt.plot(x, y, 'ko', markersize=8, mfc='none')
plt.plot(x, predicted_y, 'b-', 0.1)
plt.xlim([0.0, 2.1])
plt.ylim([0.0, 2.1])
plt.plot([0, 2.1], [0, 2.1], 'k--', lw=2)
plt.text(1.15, 0.7,
         'y = %0.4fx + %0.4f \nR$^2$ = %0.2f' %(coef, intercept, r_squared))
plt.xlabel('Observed OPv (DTTv)')
plt.ylabel('Predicted OPv (DTTv)')
plt.show()