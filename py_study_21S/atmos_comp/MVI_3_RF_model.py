import pandas as pd
import numpy as np


case = '1_Basic_1_Seoul'

df = pd.read_csv('C:\\Users\\Haley\\Dropbox\\패밀리룸\\MVI\\Data\\'+case+'_raw.csv')
scalingfactor = {}
data_scaled = df.copy()

for c in df.columns[1:]:
    denominator = df[c].max()-df[c].min()
    scalingfactor[c] = [denominator, df[c].min(), df[c].max()]
    data_scaled[c] = (df[c] - df[c].min())/denominator

data_wodate_scaled = data_scaled.iloc[:, 1:]
dft = data_wodate_scaled.to_numpy()

# seeds = [777, 1004, 322, 224, 417]
seeds = [777, 1004, 322]
ions = ['SO42-', 'NO3-', 'Cl-', 'Na+', 'NH4+', 'K+', 'Mg2+', 'Ca2+']
ocec = ['OC', 'EC']
elementals = ['S', 'K', 'Ca', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Ni', 'Cu', 'Zn', 'As', 'Se', 'Br', 'Pb']

elements = [ions,ocec,elementals, ions+ocec, ions+elementals, ocec+elementals,ions+ocec+elementals]
elements_name = ['ions', 'ocec','elementals','ion-ocec','ion-elementals','ocec-elementals','ions-ocec-elementals']

iteration = 1

for s in range(len(seeds)):
    for ele in range(len(elements)):
        for iter in range(iteration):

            name = case + '_result_'+ str(seeds[s])+'_RF_'+str(elements_name[ele])+'_'+str(iter+1)

            eraser = data_wodate_scaled.sample(int(len(data_wodate_scaled)*0.2), random_state=seeds[s]).index.tolist()
            target = elements[ele]
#            data_wodate_scaled[np.ix_(eraser, target)] = np.nan
            data_wodate_scaled.loc[eraser, target] = np.nan

            import sklearn.neighbors._base
            sys.modules['sklearn.neighbors.base'] = sklearn.neighbors._base
            from missingpy import MissForest

            # Make an instance and perform the imputation
            imputer = MissForest()
            # x = df.drop(df.columns[[0, 1, 2, 3]], axis=1)
            x_imputed = imputer.fit_transform(data_wodate_scaled)

            data_array = x_imputed
            column_names = ['PM2.5', 'SO42.', 'NO3.', 'Cl.',
                            'Na.', 'NH4.', 'K.', 'Mg2.', 'Ca2.', 'OC', 'EC', 'Si', 'S', 'K', 'Ca',
                            'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Ni', 'Cu', 'Zn', 'As', 'Se', 'Br', 'Ba',
                            'Pb', 'PM10']
            result = pd.DataFrame(data_array, columns=column_names)
            result.isnull().sum()

            # Add imputed values as columns to the untouched dataset
            df_test['MF_OC'] = x_imputed[:, 9]
            df_test['MF_EC'] = x_imputed[:, 10]
            comparison_df = df_test[['OC', 'MF_OC', 'EC', 'MF_EC']]

            # Calculate absolute errors
            comparison_df['ABS_ERROR_OC'] = np.abs(comparison_df['OC'] - comparison_df['MF_OC'])
            comparison_df['ABS_ERROR_EC'] = np.abs(comparison_df['EC'] - comparison_df['MF_EC'])
            comparison_df.head()

            # Show only rows where imputation was performed
            imputation_result = comparison_df.iloc[sorted([*inds1])]
            imputation_result.to_csv("imputation_result_OC.csv")

            x = x_imputed[inds1, 9]
            y = df_test.iloc[inds1]
            y = y['OC']

            from sklearn import linear_model
            import sklearn

            x = np.array(x)
            y = np.array(y)

            # Create linear regression object
            linreg = linear_model.LinearRegression()
            # Fit the linear regression model
            model = linreg.fit(x.reshape(-1, 1), y.reshape(-1, 1))
            # Get the intercept and coefficients
            intercept = model.intercept_
            coef = model.coef_
            result = [intercept, coef]
            predicted_y = x.reshape(-1, 1) * coef + intercept
            r_squared = sklearn.metrics.r2_score(y, predicted_y)
            print(r_squared)



            x_train = np.array(data_wodate_scaled.drop(index=data_wodate_scaled.index[eraser], columns=target))