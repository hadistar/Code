import matplotlib.pyplot as plt
from matplotlib import rcParams
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 13
rcParams.update({'figure.autolayout': True})
plt.figure()
# ratio = [1,0, 16, 49, 3, 5, 20,
#          2, 4, 16]
ratio = [4, 16, 16,  2, 3,  49, 20,
         5, 1]
labels = ["Secondary nitrate", "Secondary sulrfate", "Traffic", "Heating", "Biomass burning", "Coal combustion", "Industry (oil)",
                     "Industry (smelting)", "Sea Salts"]
colors = ['C9','C8','C7','C6','C5','C4','C3','C2','C1']

# labels = ["Salts", "Soil", "SS", "Coal combustion", "Biomass burning", "Industry Smelting", "Industry Oil",
#                      "Heating", "SN", "Mobile"]
# colors = ['C1','C0','C8','C4','C5','C2','C3','C6','C9','C7']
plt.pie(ratio, autopct='%.1f%%',colors=colors,textprops={'fontsize': 10},explode=(0, 0 ,0,0,0,0,
                                                                                  0,0,0))
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, labels=labels, borderaxespad=0.)
plt.savefig('D:\\GitHub\\Code\\python_plot\\pie_source.png')
plt.show()

import matplotlib.pyplot as plt
from matplotlib import rcParams
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 13
rcParams.update({'figure.autolayout': True})
plt.figure()
ratio = [24.31, 18.75, 18.83, 12.55, 11.76, 3.63, 1.79, 4.03, 2.68, 1.66]
labels = ["Secondary nitrate", "Secondary sulrfate", "Traffic", "Heating", "Biomass burning", "Coal combustion", "Industry (Oil)",
                     "Industry (smelting)", "Sea Salts", "Soil"]
colors = ['C9','C8','C7','C6','C5','C4','C3','C2','C1','C0']
plt.pie(ratio, autopct='%.1f%%',colors=colors,textprops={'fontsize': 10},explode=(0,0,0,0,0,0,
                                                                                  0,0,0,0))
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, labels=labels, borderaxespad=0.)
plt.savefig('D:\\GitHub\\Code\\python_plot\\pie_source.png')
plt.show()