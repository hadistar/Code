import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MaxNLocator

# data import
df = pd.read_csv('C:\\Users\\haley\\github\\R\\python_plot\\rdata.csv').dropna()

# assign font family
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 13

print(df.columns)
df_ilcr = df.iloc[:, [2, 3, 4, 5, 168]]
df_ilcr.head(10)
df_ilcr.columns = ["As","Cr6","Ni","Pb","Season"]
print(df_ilcr.columns)

#stack bar for ILCR
x= df_ilcr[['Season','As','Cr6','Ni','Pb']]
y= x.set_index('Season')
z=y.groupby('Season').mean()

fig = z.plot.bar(stacked=True)
fig.set_ylabel('Incremental Lifetime Cancer Risk ('+ "x 10" + '$^{-4}$'+')')
fig.legend(loc="upper left", bbox_to_anchor=(0.55,1), fontsize=10)
plt.xticks(rotation=40, size=10)
patterns = [ "/" , "\\" , "|" , "-"]
# dif = fig.add_subplot(111)
for i in range(len(patterns)):
    fig.bar(i, 3, edgecolor='black', hatch=patterns[i])

plt.show()