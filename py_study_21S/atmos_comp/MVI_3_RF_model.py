import pandas as pd
import numpy as np
import sklearn.neighbors._base
sys.modules['sklearn.neighbors.base'] = sklearn.neighbors._base
from missingpy import MissForest


case = '3_AP_3_Ulsan'

df = pd.read_csv('C:\\Users\\Haley\\Dropbox\\패밀리룸\\MVI\\Data\\'+case+'_raw.csv')
scalingfactor = {}
data_scaled = df.copy()

for c in df.columns[1:]:
    denominator = df[c].max()-df[c].min()
    scalingfactor[c] = [denominator, df[c].min(), df[c].max()]
    data_scaled[c] = (df[c] - df[c].min())/denominator

data_wodate_scaled = data_scaled.iloc[:, 1:]

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

            data_wodate_scaled.loc[eraser, target] = np.nan
            # Make an instance and perform the imputation
            imputer = MissForest()
            # x = df.drop(df.columns[[0, 1, 2, 3]], axis=1)
            x_imputed = imputer.fit_transform(data_wodate_scaled)

            column_names = ['PM2.5', 'SO42-', 'NO3-', 'Cl-', 'Na+', 'NH4+', 'K+', 'Mg2+',
                            'Ca2+', 'OC', 'EC', 'S', 'K', 'Ca', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Ni',
                            'Cu', 'Zn', 'As', 'Se', 'Br', 'Pb', 'month', 'hour', 'weekday', 'PM25',
                            'PM10', 'SO2', 'CO', 'O3', 'NO2']
            result = pd.DataFrame(x_imputed, columns=column_names)
            result= result.loc[:, target]
            for c in result:
                result[c] = result[c] * scalingfactor[c][0] + scalingfactor[c][1]

            result.to_csv(name + '.csv', index=False)