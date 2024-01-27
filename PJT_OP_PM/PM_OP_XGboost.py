import xgboost

import warnings
from scipy.stats import pearsonr
from sklearn.impute import KNNImputer
from sklearn.model_selection import train_test_split
import keras
from keras import layers
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM, Bidirectional, GRU
from keras.models import Model
from keras.layers import Input
from keras.layers import Flatten
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
import IPython
import keras_tuner as kt
import shutil
from keras.layers import LeakyReLU
LeakyReLU = LeakyReLU(alpha=0.1)
from sklearn.ensemble import RandomForestRegressor
# from hyperopt import tpe, hp, Trials
# from hyperopt.fmin import fmin
from sklearn.metrics import mean_squared_error, mean_absolute_error
def get_rmse(y_valid, y_predict):
    return np.sqrt(mean_squared_error(y_valid, y_predict))


warnings.filterwarnings('ignore')

# import dtale # EDA tool

# df = pd.read_csv('D:\\OneDrive - SNU\\3.py_SCH\\data\\PM2.5_OP_2019-2021_2.csv')

df = pd.read_csv('data/PM2.5_OP_2019-2021_2.csv') # when using server

# 황사일 제거시
# df = df[df['황사여부']==0]

# dtale.show(df)

# df_y = df[['OPv (DTTv)', 'OPm (DTTm)']]
df_y = df[['OPv (DTTv)']]

df_x = df[['온도', '습도', '풍속', 'O3', 'NO2', 'CO', 'PM2.5', 'PM10',
       'OC', 'EC', 'TC', 'WSTN', 'WSIN', 'WSON', 'WSOC', 'Cl', 'NO3', 'SO4',
       'Na', 'NH4', 'K', 'Ca', 'Mg', 'acidity', 'Li', 'Al', 'Ti', 'V', 'Cr',
       'Mn', 'Fe', 'Ni', 'Cu', 'Zn', 'As', 'Cd', 'Pb', 'SO2']]

df_x.isna().sum().sum()

imputer = KNNImputer(n_neighbors=3) #KNN
df_x.iloc[:,:] = imputer.fit_transform(df_x)

df_x.isna().sum().sum()

# r,_=pearsonr(df_y.iloc[:,0],df_y.iloc[:,1])
# print(r**2)

df = pd.concat([df_x,df_y], axis=1)



scalingfactor = {}
data_scaled = df.copy()

for c in df.columns[:]:
    denominator = df[c].max()-df[c].min()
    scalingfactor[c] = [denominator, df[c].min(), df[c].max()]
    data_scaled[c] = (df[c] - df[c].min())/denominator

df = data_scaled.iloc[:, :]

target = ['OPv (DTTv)']

df_y = df[['OPv (DTTv)']]

df_x = df[['온도', '습도', '풍속', 'O3', 'NO2', 'CO', 'PM2.5', 'PM10',
       'OC', 'EC', 'TC', 'WSTN', 'WSIN', 'WSON', 'WSOC', 'Cl', 'NO3', 'SO4',
       'Na', 'NH4', 'K', 'Ca', 'Mg', 'acidity', 'Li', 'Al', 'Ti', 'V', 'Cr',
       'Mn', 'Fe', 'Ni', 'Cu', 'Zn', 'As', 'Cd', 'Pb', 'SO2']]

# PM25,PM10 제거시
df_x = df[['온도', '습도', '풍속', 'O3', 'NO2', 'CO',
       'OC', 'EC', 'TC', 'WSTN', 'WSIN', 'WSON', 'WSOC', 'Cl', 'NO3', 'SO4',
       'Na', 'NH4', 'K', 'Ca', 'Mg', 'acidity', 'Li', 'Al', 'Ti', 'V', 'Cr',
       'Mn', 'Fe', 'Ni', 'Cu', 'Zn', 'As', 'Cd', 'Pb', 'SO2']]

x_train, x_test, y_train, y_test = train_test_split(df_x, df_y, test_size=0.2, random_state=7)

model = xgboost.XGBRegressor(n_estimators=30, learning_rate=0.005, gamma=0, subsample=0.75,
                           colsample_bytree=0.4, max_depth=10)

# Train the model
model.fit(x_train,y_train)

# Predict

y_predicted = model.predict(x_test)

y_pred_train = model.predict(x_train.values)
y_pred_valid = model.predict(x_test.values)
print("Y Pred Train Shape : ", y_pred_train.shape)
print("Y Pred Test  Shape : ", y_pred_valid.shape)

train_mse = mean_squared_error(y_train,y_pred_train)
valid_mse = mean_squared_error(y_test,y_pred_valid)
print('Train MSE : {0}'.format(train_mse))
print('Test  MSE : {0}'.format(valid_mse))

train_rmse = get_rmse(y_train,y_pred_train)
valid_rmse = get_rmse(y_test,y_pred_valid)
print('Train RMSE : {0}'.format(train_rmse))
print('Test  RMSE : {0}'.format(valid_rmse))

train_mae = mean_absolute_error(y_train,y_pred_train)
valid_mae = mean_absolute_error(y_test,y_pred_valid)
print('Train MAE : {0}'.format(train_mae))
print('Test  MAE : {0}'.format(valid_mae))

from scipy import stats
train_r2 = stats.pearsonr(np.array(y_train).flatten(), y_pred_train.flatten()).statistic**2
valid_r2 = stats.pearsonr(np.array(y_test).flatten(), y_pred_valid.flatten()).statistic**2
# train_r2 = r2_score(np.array(y_train), y_pred_train)
# valid_r2 = r2_score(y_test, y_pred_valid)
print('Train R2  : {0}'.format(train_r2))
print('Test  R2  : {0}'.format(valid_r2))

y_predicted = model.predict(x_test)