import numpy as np
import pandas as pd

iris = pd.read_csv('iris.csv')

# Keep an untouched copy for later
iris_orig = iris.copy()

iris.head()


# Generate unique lists of random integers
inds1 = list(set(np.random.randint(0, len(iris), 10)))
inds2 = list(set(np.random.randint(0, len(iris), 15)))

# Replace the values at given index position with NaNs
iris['sepal_length'] = [val if i not in inds1 else np.nan for i, val in enumerate(iris['sepal_length'])]
iris['petal_width'] = [val if i not in inds2 else np.nan for i, val in enumerate(iris['petal_width'])]

# Get count of missing values by column
iris.isnull().sum()

from missingpy import MissForest

# Make an instance and perform the imputation
imputer = MissForest()
X = iris.drop('species', axis=1)
X_imputed = imputer.fit_transform(X)

# Add imputed values as columns to the untouched dataset
iris_orig['MF_sepal_length'] = X_imputed[:, 0]
iris_orig['MF_petal_width'] = X_imputed[:, -1]
comparison_df = iris_orig[['sepal_length', 'MF_sepal_length', 'petal_width', 'MF_petal_width']]

# Calculate absolute errors
comparison_df['ABS_ERROR_sepal_length'] = np.abs(compaison_df['sepal_length'] - comparison_df['MF_sepal_length'])
comparison_df['ABS_ERROR_petal_width'] = np.abs(compaison_df['petal_width'] - comparison_df['MF_petal_width'])

# Show only rows where imputation was performed
comparison_df.iloc[sorted([*inds1, *inds2])]