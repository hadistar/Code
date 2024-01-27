from sklearn.impute import KNNImputer
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

from sklearn.metrics import mean_squared_error, mean_absolute_error
def get_rmse(y_valid, y_predict):
    return np.sqrt(mean_squared_error(y_valid, y_predict))

df = pd.read_csv('D:\\OneDrive\\3.py_SCH\\data_OP_ML\\PM2.5_OP_2019-2021_2.csv')

# 황사일 제거시(To exclude data for cases of yellow dust, please execute the following line)
# df = df[df['황사여부']==0]

df_y = df[['OPv (DTTv)']]

df_x = df[['온도', '습도', '풍속', 'O3', 'NO2', 'CO', 'PM2.5', 'PM10',
       'OC', 'EC', 'TC', 'WSTN', 'WSIN', 'WSON', 'WSOC', 'Cl', 'NO3', 'SO4',
       'Na', 'NH4', 'K', 'Ca', 'Mg', 'acidity', 'Li', 'Al', 'Ti', 'V', 'Cr',
       'Mn', 'Fe', 'Ni', 'Cu', 'Zn', 'As', 'Cd', 'Pb', 'SO2']]

imputer = KNNImputer(n_neighbors=3) #KNN
df_x.iloc[:,:] = imputer.fit_transform(df_x)

df = pd.concat([df_x,df_y], axis=1)

scalingfactor = {}
data_scaled = df.copy()

for c in df.columns[:]:
    denominator = df[c].max()-df[c].min()
    scalingfactor[c] = [denominator, df[c].min(), df[c].max()]
    data_scaled[c] = (df[c] - df[c].min())/denominator

df = data_scaled.iloc[:, :]

df_y = df[['OPv (DTTv)']]

df_x = df[['온도', '습도', '풍속', 'O3', 'NO2', 'CO', 'PM2.5', 'PM10',
       'OC', 'EC', 'TC', 'WSTN', 'WSIN', 'WSON', 'WSOC', 'Cl', 'NO3', 'SO4',
       'Na', 'NH4', 'K', 'Ca', 'Mg', 'acidity', 'Li', 'Al', 'Ti', 'V', 'Cr',
       'Mn', 'Fe', 'Ni', 'Cu', 'Zn', 'As', 'Cd', 'Pb', 'SO2']]

x_train, x_test, y_train, y_test = train_test_split(df_x, df_y, test_size=0.2, random_state=7)

df_before = pd.concat([x_train,y_train], axis=1)
df_before2 = pd.concat([df_before,x_test], axis=0)

imputer = KNNImputer(n_neighbors=3) #KNN
df_before2.iloc[:,:] = imputer.fit_transform(df_before2)

y_pred_valid= df_before2.loc[x_test.index.values].iloc[:,-1]

valid_mse = mean_squared_error(y_test,y_pred_valid)
print('Test  MSE : {0}'.format(valid_mse))

valid_rmse = get_rmse(y_test,y_pred_valid)
print('Test  RMSE : {0}'.format(valid_rmse))

valid_mae = mean_absolute_error(y_test,y_pred_valid)
print('Test  MAE : {0}'.format(valid_mae))

from scipy import stats
valid_r2 = stats.pearsonr(np.array(y_test).flatten(), y_pred_valid).statistic**2
print('Test  R2  : {0}'.format(valid_r2))

