import numpy as np
import pandas as pd
import warnings
from scipy.stats import pearsonr
from sklearn.impute import KNNImputer
from sklearn.model_selection import train_test_split

warnings.filterwarnings('ignore')

# import dtale # EDA tool

# df = pd.read_csv('D:\\OneDrive - SNU\\3.py_SCH\\data\\PM2.5_OP_2019-2021_2.csv')

df = pd.read_csv('data/PM2.5_OP_2019-2021_2.csv') # when using server

# 황사일 제거시
df = df[df['황사여부']==0]

# dtale.show(df)

df_y = df[['OPv (DTTv)', 'OPm (DTTm)']]
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

# target = ['OPv (DTTv)', 'OPm (DTTm)']
target = ['OPv (DTTv)']

df_y = df[['OPv (DTTv)']]

df_x = df[['온도', '습도', '풍속', 'O3', 'NO2', 'CO', 'PM2.5', 'PM10',
       'OC', 'EC', 'TC', 'WSTN', 'WSIN', 'WSON', 'WSOC', 'Cl', 'NO3', 'SO4',
       'Na', 'NH4', 'K', 'Ca', 'Mg', 'acidity', 'Li', 'Al', 'Ti', 'V', 'Cr',
       'Mn', 'Fe', 'Ni', 'Cu', 'Zn', 'As', 'Cd', 'Pb', 'SO2']]

# PM25,PM10 제거시
# df_x = df[['온도', '습도', '풍속', 'O3', 'NO2', 'CO',
#        'OC', 'EC', 'TC', 'WSTN', 'WSIN', 'WSON', 'WSOC', 'Cl', 'NO3', 'SO4',
#        'Na', 'NH4', 'K', 'Ca', 'Mg', 'acidity', 'Li', 'Al', 'Ti', 'V', 'Cr',
#        'Mn', 'Fe', 'Ni', 'Cu', 'Zn', 'As', 'Cd', 'Pb', 'SO2']]

x_train, x_test, y_train, y_test = train_test_split(df_x, df_y, test_size=0.2, random_state=7)

'''
#Kfold 쓴다면(cross validation)
import numpy as np
from sklearn.model_selection import KFold

kf = KFold(n_splits=2)

for train_index, test_index in kf.split(X):
    print("TRAIN:", train_index, "TEST:", test_index)
    X_train, X_test = x[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

'''


##하이퍼 파라미터 최적화

from sklearn.ensemble import RandomForestRegressor
# from hyperopt import tpe, hp, Trials
# from hyperopt.fmin import fmin
from sklearn.metrics import mean_squared_error, mean_absolute_error
def get_rmse(y_valid, y_predict):
    return np.sqrt(mean_squared_error(y_valid, y_predict))

param_grid = {'n_estimators':[30], # 10~2000
             'max_features':[5], # 1~30
             'min_samples_leaf': [2], # 1~30
             'min_samples_split': [2], # 1~30
             'max_depth': [10] # 1~30
              }

# param_grid = {'n_estimators':[10,20,30,100,500], # 10~2000
#              'max_features':[1,3,5,10,20], # 1~30
#              'min_samples_leaf': [2,5,10], # 1~30
#              'min_samples_split': [2,5,10], # 1~30
#              'max_depth': [1,2,3,10] # 1~30
#               }


# Grid serach와 Hyperopt로 찾음

from sklearn.model_selection import GridSearchCV

rf_regr = RandomForestRegressor(n_estimators=50, max_depth=20, min_samples_leaf=3,
                                  min_samples_split=3, max_features=10, n_jobs=-1,random_state=7)


grid_search = GridSearchCV(rf_regr,param_grid,cv=5,scoring='r2')
# grid_search = rf_regr.fit(x_train,y_train)

grid_search.fit(x_train,y_train)
print(grid_search.best_params_)

y_pred_train = grid_search.predict(x_train.values)
y_pred_valid = grid_search.predict(x_test.values)
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
train_r2 = stats.pearsonr(np.array(y_train).flatten(), y_pred_train).statistic**2
valid_r2 = stats.pearsonr(np.array(y_test).flatten(), y_pred_valid).statistic**2
# train_r2 = r2_score(np.array(y_train), y_pred_train)
# valid_r2 = r2_score(y_test, y_pred_valid)
print('Train R2  : {0}'.format(train_r2))
print('Test  R2  : {0}'.format(valid_r2))

y_predicted = grid_search.predict(x_test)
evaluation = grid_search.score(x_test, y_test)

f = open('result.txt', 'w')
f.write(f"""
    Hyperparameters
    : {grid_search.get_params()}
    R2 = {evaluation}.
    Y Pred Train Shape : {y_pred_train.shape}
    Y Pred Test  Shape : {y_pred_valid.shape}
    Train MSE : {train_mse}
    Test  MSE : {valid_mse}
    Train RMSE : {train_rmse}
    Test  RMSE : {valid_rmse}
    Train MAE : {train_mae}
    Test  MAE : {valid_mae}
    Train R2  : {train_r2}
    Test  R2  : {valid_r2}
    """)
f.close()

# rescaling
# x = x' * (max-min) + min
# saving scaling factor in [max-min, min, max]

y_predicted_total = grid_search.predict(np.array(df_x))
y_predicted_total = pd.DataFrame(y_predicted_total, columns=target)

for c in y_predicted_total:
    y_predicted_total[c] = y_predicted_total[c] * scalingfactor[c][0] + scalingfactor[c][1]

y_predicted_total.to_csv('result_test.csv', index=False)



# Feature importance

# feature_importance = grid_search.feature_importances_

fi=pd.concat([pd.DataFrame(df_x.columns), pd.DataFrame(feature_importance)], axis=1)

fi.to_clipboard()