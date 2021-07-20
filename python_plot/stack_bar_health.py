import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
import pandas as pd
import numpy as np

# data import
df = pd.read_csv('D:\\GitHub\\Code\\python_plot\\rdata.csv').dropna()
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
df["Season2"] = "Annual"

# assign font family
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 13

print(df.columns)
df_ilcr = df.iloc[:, [2, 3, 4, 5, 168,169]]
df_ilcr.head(10)
df_ilcr.columns = ["As","Cr6","Ni","Pb","Season","Season2"]
print(df_ilcr.columns)

# Calculate mean for each season
x= df_ilcr[['Season','As','Cr6','Ni','Pb']]
y= x.set_index('Season')
z = y.groupby(['Season']).mean().reset_index()

# Calculate mean for annual
x2 = df_ilcr[['Season2','As','Cr6','Ni','Pb']]
y2 = x2.groupby(['Season2']).mean().reset_index()
y2 = y2.rename(columns={'Season2':'Season'})

z = pd.concat([z,y2], ignore_index=True)

# Order Season names in the table
Season = ['Autumm', 'Winter','Spring', 'Summer','Annual']
mapping = {Season: i for i, Season in enumerate(Season)}
key = z['Season'].map(mapping)
z = z.iloc[key.argsort()]
z.iloc[:,1:5] =z.iloc[:,1:5]*10e5
z
# Draw the bar chart
plt.grid(True)
plt.rcParams['axes.axisbelow'] = True
plt.bar(Season, z.Pb, color='red',width=0.6,label='Pb',bottom=z.Ni+z.Cr6+z.As)
plt.bar(Season, z.Ni, color='green',label='Ni',width=0.6,bottom=z.Cr6+z.As) # stacked bar chart
plt.bar(Season, z.Cr6, color='orange',label='Cr6',width=0.6,bottom=z.As) # stacked bar chart
plt.bar(Season, z.As, color='blue',label='As', width=0.6) # stacked bar chart
plt.ylabel('Incremental Lifetime Cancer Risk ('+ "x 10" + '$^{-6}$'+')',fontsize=15)
plt.xticks(Season,rotation=40, size=10)
plt.legend(loc="upper left", bbox_to_anchor=(0.8,1), fontsize=10)
plt.show()