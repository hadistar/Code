import matplotlib.pyplot as plt
import pandas as pd

# data import
df = pd.read_csv('C:\\Users\\haley\\github\\R\\python_plot\\rdata.csv').dropna()
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

# Use Dan's trick to order Season names in the table created by groupby
z = y.groupby(['Season']).mean().reset_index()
Season = ['Autumm', 'Winter','Spring', 'Summer']
mapping = {Season: i for i, Season in enumerate(Season)}
key = z['Season'].map(mapping)
z = z.iloc[key.argsort()]

# Draw the bar chart
fig = z.plot.bar(stacked=True, x='Season')
fig.set_ylabel('Incremental Lifetime Cancer Risk ('+ "x 10" + '$^{-6}$'+')')
#  reverse lavels
handles,labels = fig.get_legend_handles_labels()
fig.legend(reversed(handles), reversed(labels), loc="upper left", bbox_to_anchor=(0.8,1), fontsize=10)
plt.xticks(rotation=40, size=10)
plt.show()