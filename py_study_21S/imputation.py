from sklearn.datasets import load_iris
import numpy as np
import pandas as pd

iris = load_iris()

# feature_names 와 target을 레코드로 갖는 데이터프레임 생성
df = pd.DataFrame(data=iris.data, columns=iris.feature_names)

# Keep an untouched copy for later
df_orig = df.copy()
df.head(2)
df.columns
df.columns = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
df_orig.columns = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
# Generate unique lists of random integers
inds1 = list(set(np.random.randint(0, len(df), 10)))
inds2 = list(set(np.random.randint(0, len(df), 15)))

# Replace the values at given index position with NaNs
df['sepal_length'] = [val if i not in inds1 else np.nan for i, val in enumerate(df['sepal_length'])]
df['petal_width'] = [val if i not in inds2 else np.nan for i, val in enumerate(df['petal_width'])]

# Get count of missing values by column
df.isnull().sum()

import sklearn.neighbors._base
sys.modules['sklearn.neighbors.base'] = sklearn.neighbors._base
from missingpy import MissForest

# Make an instance and perform the imputation
imputer = MissForest()
# x = df.drop('species', axis=1)
X_imputed = imputer.fit_transform(df)

# Add imputed values as columns to the untouched dataset
df_orig['MF_sepal_length'] = X_imputed[:, 0]
df_orig['MF_petal_width'] = X_imputed[:, -1]
comparison_df = df_orig[['sepal_length', 'MF_sepal_length', 'petal_width', 'MF_petal_width']]

# Calculate absolute errors
comparison_df['ABS_ERROR_sepal_length'] = np.abs(comparison_df['sepal_length'] - comparison_df['MF_sepal_length'])
comparison_df['ABS_ERROR_petal_width'] = np.abs(comparison_df['petal_width'] - comparison_df['MF_petal_width'])

# Show only rows where imputation was performed
comparison_df.iloc[sorted([*inds1, *inds2])]