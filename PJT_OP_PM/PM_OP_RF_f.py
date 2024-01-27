import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

from scipy import stats

def get_rmse(y_valid, y_predict):
    return np.sqrt(mean_squared_error(y_valid, y_predict))

df = pd.read_csv('D:\\OneDrive\\3.py_SCH\\data_OP_ML\\PM2.5_OP_2019-2021_2.csv')

# 황사일 제거시(To exclude data for cases of yellow dust, please execute the following line)
df = df[df['황사여부']==0]

df_y = df[['OPv (DTTv)']]

df_x = df[['온도', '습도', '풍속', 'O3', 'NO2', 'CO', 'PM2.5', 'PM10',
       'OC', 'EC', 'TC', 'WSTN', 'WSIN', 'WSON', 'WSOC', 'Cl', 'NO3', 'SO4',
       'Na', 'NH4', 'K', 'Ca', 'Mg', 'acidity', 'Li', 'Al', 'Ti', 'V', 'Cr',
       'Mn', 'Fe', 'Ni', 'Cu', 'Zn', 'As', 'Cd', 'Pb', 'SO2']]

imputer = KNNImputer(n_neighbors=3) #KNN
df_x.iloc[:,:] = imputer.fit_transform(df_x)

df = pd.concat([df_x,df_y], axis=1)

# scalingfactor = {}
# data_scaled = df.copy()

# for c in df.columns[:]:
#     denominator = df[c].max()-df[c].min()
#     scalingfactor[c] = [denominator, df[c].min(), df[c].max()]
#     data_scaled[c] = (df[c] - df[c].min())/denominator
#
# data_wodate_scaled = data_scaled.iloc[:, :]

df_y = df[['OPv (DTTv)']]

df_x = df[['온도', '습도', '풍속', 'O3', 'NO2', 'CO', 'PM2.5', 'PM10',
       'OC', 'EC', 'TC', 'WSTN', 'WSIN', 'WSON', 'WSOC', 'Cl', 'NO3', 'SO4',
       'Na', 'NH4', 'K', 'Ca', 'Mg', 'acidity', 'Li', 'Al', 'Ti', 'V', 'Cr',
       'Mn', 'Fe', 'Ni', 'Cu', 'Zn', 'As', 'Cd', 'Pb', 'SO2']]

random_state_split= 777

x_train, x_test, y_train, y_test = train_test_split(df_x, df_y, test_size=0.2, random_state=random_state_split)

n_estimators = 30
max_depth = 10
min_samples_leaf = 2
min_samples_split = 2
max_features = 5
#random_state= 1000

model = RandomForestRegressor(n_estimators=n_estimators,
                              max_depth=max_depth,
                              max_features=max_features,
                              min_samples_leaf=min_samples_leaf,
                              min_samples_split=min_samples_split,
#                              random_state=random_state,
                              n_jobs=-1)

model.fit(x_train, y_train)


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

# train_r2 = r2_score(np.array(y_train).reshape(-1,1), np.array(y_pred_train).reshape(-1,1))
# valid_r2 = r2_score(y_test, y_pred_valid)

train_r2 = stats.pearsonr(np.array(y_train).flatten(), y_pred_train).statistic**2
valid_r2 = stats.pearsonr(np.array(y_test).flatten(), y_pred_valid).statistic**2

print('Train R2  : {0}'.format(train_r2))
print('Test  R2  : {0}'.format(valid_r2))



y_predicted = model.predict(x_test)
evaluation = model.score(x_test, y_test)

f = open('result_.txt', 'w')
f.write(f"""
    The hyperparameter search is complete. 
    The best hyperparameters
     - n_estimators: {n_estimators}
     - max_depth: {max_depth}
     - min_samples_leaf: {min_samples_leaf}
     - min_samples_split: {min_samples_split}
     - max_features: {max_features}
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

# y_predicted_total = model.predict(np.array(data_wodate_scaled[df_x.columns]))
# y_predicted_total = pd.DataFrame(y_predicted_total, columns=target)
#
# y_pred_test = pd.DataFrame()
#
# for c in y_predicted_total:
#     y_predicted_total[c] = y_predicted_total[c] * scalingfactor[c][0] + scalingfactor[c][1]
#     y_pred_test[c] = y_pred_valid * scalingfactor[c][0] + scalingfactor[c][1]
#
# y_predicted_total.to_csv('result_test_.csv', index=False)


# Feature importance

# feature_importance = model.feature_importances_
#
# fi=pd.concat([pd.DataFrame(df_x.columns), pd.DataFrame(feature_importance)], axis=1)
# fi.to_clipboard(excel=True, sep=None, index=False, header=None)

pd.DataFrame([train_r2,train_rmse,train_mae,valid_r2,valid_rmse,valid_mae]).T.to_clipboard(excel=True, sep=None, index=False, header=None)
#
#
# pd.concat([pd.DataFrame(y_train.reset_index(drop=True)),pd.DataFrame(y_pred_train)], axis=1, ignore_index=True).to_csv('result_RF_trainset.csv', index=False)
# pd.concat([pd.DataFrame(y_test.reset_index(drop=True)),pd.DataFrame(y_pred_valid)], axis=1, ignore_index=True).to_csv('result_RF_testset.csv', index=False)