import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
import pandas as pd
# import numpy as np

# data import
df = pd.read_csv('D:\\GitHub\\Code\\python_plot\\rdata.csv').dropna()
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
df["Season2"] = "Annual"

# assign font family
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 13

print(df.columns)
# df_ilcr = df.iloc[:, [2, 3, 4, 5, 168,169]]
df_ilcr = df.iloc[:, [7, 8, 9, 10, 11, 12, 13, 14, 15, 168, 169]]
df_ilcr.head(10)
# df_ilcr.columns = ["As","Cr6","Ni","Pb","Season","Season2"]
df_ilcr.columns = ["As","Cr6","Cr3","Cu","Ni","Pb","Zn","V","Mn",'Season', 'Season2']
print(df_ilcr.columns)

# Calculate mean for each season
# x= df_ilcr[['Season','As','Cr6','Ni','Pb']]
x= df_ilcr[['Season',"As","Cr6","Cr3","Cu","Ni","Pb","Zn","V","Mn"]]
y= x.set_index('Season')
z = y.groupby(['Season']).mean().reset_index()

# Calculate mean for annual
# x2 = df_ilcr[['Season2','As','Cr6','Ni','Pb']]
x2= df_ilcr[['Season2',"As","Cr6","Cr3","Cu","Ni","Pb","Zn","V","Mn"]]
y2 = x2.groupby(['Season2']).mean().reset_index()
y2 = y2.rename(columns={'Season2':'Season'})

z = pd.concat([z,y2], ignore_index=True)

# Order Season names in the table
Season = ['Autumm', 'Winter','Spring', 'Summer','Annual']
mapping = {Season: i for i, Season in enumerate(Season)}
key = z['Season'].map(mapping)
z = z.iloc[key.argsort()]
# z.iloc[:,1:5] =z.iloc[:,1:5]*10e5

# Draw the bar chart
# plt.figure()
# plt.grid(True, linestyle="--")
# plt.rcParams['axes.axisbelow'] = True
# plt.bar(Season, z.Pb, color='red',width=0.6,label='Pb',bottom=z.Ni+z.Cr6+z.As)
# plt.bar(Season, z.Ni, color='green',label='Ni',width=0.6,bottom=z.Cr6+z.As) # stacked bar chart
# plt.bar(Season, z.Cr6, color='orange',label='Cr$^{6+}$',width=0.6,bottom=z.As) # stacked bar chart
# plt.bar(Season, z.As, color='blue',label='As', width=0.6) # stacked bar chart
# plt.ylabel('Incremental Lifetime Cancer Risk ('+ "x 10" + '$^{-6}$'+')',fontsize=15)
# plt.xticks(Season,rotation=40, size=10)
# plt.legend(loc="upper left", bbox_to_anchor=(0.62,1), fontsize=10)
# plt.savefig('D:\\GitHub\\Code\\python_plot\\ILCR_con.png')
# plt.show()

plt.figure()
plt.grid(True, linestyle="--")
plt.rcParams['axes.axisbelow'] = True
plt.bar(Season, z.Zn, color='C9',width=0.6,label='Zn',bottom=z.V+z.Cu+z.Cr3+z.Ni+z.Pb+z.Cr6+z.Mn+z.As)
plt.bar(Season, z.V, color='C8',label='V',width=0.6,bottom=z.Cu+z.Cr3+z.Ni+z.Pb+z.Cr6+z.Mn+z.As) # stacked bar chart
plt.bar(Season, z.Cu, color='C7',label='Cu',width=0.6,bottom=z.Cr3+z.Ni+z.Pb+z.Cr6+z.Mn+z.As) # stacked bar chart
plt.bar(Season, z.Cr3, color='C6',label='Cr$^{3+}$', width=0.6,bottom=z.Ni+z.Pb+z.Cr6+z.Mn+z.As) # stacked bar chart
plt.bar(Season, z.Ni, color='C4',label='Ni', width=0.6,bottom=z.Pb+z.Cr6+z.Mn+z.As)
plt.bar(Season, z.Pb, color='C3',label='Pb', width=0.6,bottom=z.Cr6+z.Mn+z.As)
plt.bar(Season, z.Cr6, color='C2',label='Cr$^{6+}$', width=0.6,bottom=z.Mn+z.As)
plt.bar(Season, z.Mn, color='C1',label='Mn', width=0.6,bottom=z.As)
plt.bar(Season, z.As, color='C0',label='As', width=0.6)
plt.ylabel('Hazard Quotient',fontsize=15)
plt.xticks(Season,rotation=40, size=10)
plt.legend(loc="upper left", bbox_to_anchor=(1,1), fontsize=10)
plt.savefig('D:\\GitHub\\Code\\python_plot\\Hazard_Quotient.png')
plt.show()