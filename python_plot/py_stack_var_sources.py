import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
import pandas as pd

# data import
df = pd.read_csv('D:\\GitHub\\Code\\python_plot\\rdata.csv').dropna()
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
df["Season2"] = "Annual"

# assign font family
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 13

print(df.columns)
df_ilcr = df.iloc[:, [21, 36, 51, 66, 81, 96, 111, 126, 141, 156, 168, 169]]
df_ilcr.head(10)
df_ilcr.columns = ["sa", "so", "ss", "cc", "bb", "ism", "io",
                    "h", "sn", "m", "Season","Season2"]

# df_ilcr.columns = ["Salts", "Soil", "SS", "Coal combustion", "Biomass burning", "Industry Smelting", "Industry Oil",
#                    "Heating", "SN", "Mobile", "Season","Season2"]

# Calculate mean for each season
x= df_ilcr[['Season',"sa", "so", "ss", "cc", "bb", "ism", "io",
                    "h", "sn", "m"]]
y= x.set_index('Season')
z = y.groupby(['Season']).mean().reset_index()

# Calculate mean for annual
x2 = df_ilcr[['Season2',"sa", "so", "ss", "cc", "bb", "ism", "io",
                    "h", "sn", "m"]]
y2 = x2.groupby(['Season2']).mean().reset_index()
y2 = y2.rename(columns={'Season2':'Season'})

z = pd.concat([z,y2], ignore_index=True)


# Order Season names in the table created by groupby
Season = ['Autumm', 'Winter','Spring', 'Summer', 'Annual']
mapping = {Season: i for i, Season in enumerate(Season)}
key = z['Season'].map(mapping)
z = z.iloc[key.argsort()]
# z = z.sort_index(axis=1)
z.iloc[:,1:11] =z.iloc[:,1:11]*10e5

# Draw the bar chart
# ["Salts", "Soil", "SS", "Coal combustion", "Biomass burning", "Industry Smelting", "Industry Oil",
#                     "Heating", "SN", "Mobile", "Season","Season2"]
# ['Season',"sa", "so", "ss", "cc", "bb", "is", "io",
#                     "h", "sn", "Mm"]]
plt.grid(True)
plt.rcParams['axes.axisbelow'] = True
plt.bar(Season, z.sn, color='C9',width=0.6,label="SN",bottom=z.ss+z.m+z.h+z.bb+z.cc+z.io+z.ism+z.sa+z.so)
plt.bar(Season, z.ss, color='C8',width=0.6,label="SS",bottom=z.m+z.h+z.bb+z.cc+z.io+z.ism+z.sa+z.so)
plt.bar(Season, z.m, color='C7',width=0.6,label="Mobile",bottom=z.h+z.bb+z.cc+z.io+z.ism+z.sa+z.so)
plt.bar(Season, z.h, color='C6',width=0.6,label="Heating",bottom=z.bb+z.cc+z.io+z.ism+z.sa+z.so)
plt.bar(Season, z.bb, color='C5',width=0.6,label="Biomass burning",bottom=z.cc+z.io+z.ism+z.sa+z.so)
plt.bar(Season, z.cc, color='C4',width=0.6,label="Coal combustion",bottom=z.io+z.ism+z.sa+z.so)
plt.bar(Season, z.io, color='C3',width=0.6,label="Industry Oil",bottom=z.ism+z.sa+z.so)
plt.bar(Season, z.ism, color='C2',width=0.6,label="Industry smelting",bottom=z.sa+z.so)
plt.bar(Season, z.sa, color='C1',width=0.6,label="Salts",bottom=z.so)
plt.bar(Season, z.so, color='C0',width=0.6,label="Soil")
plt.ylabel('Incremental Lifetime Cancer Risk ('+ "x 10" + '$^{-6}$'+')',fontsize=15)
plt.xticks(Season,rotation=40, size=10)
plt.legend(loc="upper left", bbox_to_anchor=(1,1), fontsize=10)
plt.show()

