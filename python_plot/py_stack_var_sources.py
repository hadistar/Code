import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
import pandas as pd

# data import
df = pd.read_csv('C:\\Users\\haley\\github\\R\\python_plot\\rdata.csv').dropna()
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
df["Season2"] = "Annual"

# assign font family
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 13

print(df.columns)
df_ilcr = df.iloc[:, [21, 36, 51, 66, 81, 96, 111, 126, 141, 156, 168, 169]]
df_ilcr.head(10)
# df_ilcr.columns = ["Salts", "Soil", "SS", "Coal combustion", "Biomass burning", "Industry Smelting", "Industry Oil", "Heating", "SN", "Mobile", "Season","Season2"]
df_ilcr.columns = ["B", "A", "I", "E", "F", "C", "D", "G", "J", "H", "Season","Season2"]
df_ilcr.head()

# Calculate mean for each season
x= df_ilcr[['Season',"B", "A", "I", "E", "F", "C", "D", "G", "J", "H"]]
y= x.set_index('Season')
z = y.groupby(['Season']).mean().reset_index()

# Calculate mean for annual
x2 = df_ilcr[['Season2',"B", "A", "I", "E", "F", "C", "D", "G", "J", "H"]]
y2 = x2.groupby(['Season2']).mean().reset_index()
y2 = y2.rename(columns={'Season2':'Season'})

z = pd.concat([z,y2], ignore_index=True)


# Order Season names in the table created by groupby
Season = ['Autumm', 'Winter','Spring', 'Summer', 'Annual']
mapping = {Season: i for i, Season in enumerate(Season)}
key = z['Season'].map(mapping)
z = z.iloc[key.argsort()]
z = z.sort_index(axis=1)
# z.columns = ["Salts", "Soil", "SS", "Coal combustion", "Biomass burning", "Industry Smelting", "Industry Oil", "Heating", "SN", "Mobile", "Season"]
z.columns = ["Soil", "Salts", "Industry Smelting", "Industry Oil", "Coal combustion", "Biomass burning", "Heating", "Mobile",  "SS", "SN", "Season"]
z.iloc[:,:10] =z.iloc[:,:10]*10e5

# Draw the bar chart

fig = z.plot(stacked=True, kind='bar', x='Season')
fig.set_ylabel('Incremental Lifetime Cancer Risk ('+ "x 10" + '$^{-6}$'+')')
#reverse labels
handles,labels = fig.get_legend_handles_labels()
fig.legend(reversed(handles), reversed(labels), loc="upper left", bbox_to_anchor=(1, 1), fontsize=10)
plt.xticks(rotation=40, size=10)
plt.grid(True, color = "grey", linewidth = "1.4", linestyle = "-.")
plt.show()
