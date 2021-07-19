import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
import pandas as pd
import numpy as np

# data import
df = pd.read_csv('D:\\GitHub\\Code\\python_plot\\rdata.csv').dropna()
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

# assign font family
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 13

print(df.columns)
df_ilcr = df.iloc[:, [2, 3, 4, 5, 168]]
df_ilcr.head(10)
df_ilcr.columns = ["As","Cr6","Ni","Pb","Season"]
print(df_ilcr.columns)

# Calculate mean for each season
x= df_ilcr[['Season','As','Cr6','Ni','Pb']]
y= x.set_index('Season')

# Order Season names in the table created by groupby
z = y.groupby(['Season']).mean().reset_index()
Season = ['Autumm', 'Winter','Spring', 'Summer']
mapping = {Season: i for i, Season in enumerate(Season)}
key = z['Season'].map(mapping)
z = z.iloc[key.argsort()]
z

# Draw the bar chart
# rcParams.update({'figure.autolayout': True})
plt.grid(True)
plt.rcParams['axes.axisbelow'] = True
label = ['Autumm', 'Winter', 'Spring', 'Summer']
N = len(z['Season'].unique())
index = np.arange(N)
plt.bar(index, z.Pb, color='red',width=0.6,label='Pb',bottom=z.Ni+z.Cr6+z.As)
plt.bar(index, z.Ni, color='green',label='Ni',width=0.6,bottom=z.Cr6+z.As) # stacked bar chart
plt.bar(index, z.Cr6, color='orange',label='Cr6',width=0.6,bottom=z.As) # stacked bar chart
plt.bar(index, z.As, color='blue',label='As', width=0.6) # stacked bar chart
plt.ylabel('Incremental Lifetime Cancer Risk ('+ "x 10" + '$^{-6}$'+')',fontsize=15)
plt.xticks(index, label,rotation=40, size=10)
plt.legend(loc="upper left", bbox_to_anchor=(0.8,1), fontsize=10)
plt.show()





fig = z.plot.bar(stacked=True, x='Season',grid=False)
fig.set_ylabel('Incremental Lifetime Cancer Risk ('+ "x 10" + '$^{-6}$'+')')
#  reverse labels
handles,labels = fig.get_legend_handles_labels()
fig.legend(reversed(handles), reversed(labels), loc="upper left", bbox_to_anchor=(0.8,1), fontsize=10)

plt.xticks(rotation=40, size=10)
plt.rcParams['axes.axisbelow'] = True
plt.show()
