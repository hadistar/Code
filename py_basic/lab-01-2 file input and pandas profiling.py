
import pandas as pd  //앞으로 쓸때 걔를 줄여서 쓰려고 pd
import pandas_profiling
from scipy import stats # statistical library //  stats는 scipy안에 있는 함수임.
// 이렇게 안하면 scipy.stats.ttest_ind() // 효율성을 위해서 scipy안에 stats만 쓰기 위해서 from, import를 사용한다.
from statsmodels.stats.weightstats import ztest # statistical library for hypothesis testing
import plotly.graph_objs as go # interactive plotting library
import plotly.express as px # interactive plotting library

data = pd.read_csv("lab-01-2 file input and pandas profiling.csv")

profile = pandas_profiling.ProfileReport(data)

profile = data.profile_report(
     title="Report with only Pearson correlation",
     correlations={
         "pearson": {"calculate": True},
         "spearman": {"calculate": False},
         "kendall": {"calculate": False},
         "phi_k": {"calculate": False},
         "cramers": {"calculate": False},
     },
 )


profile.to_file('test.html')


# Z-test, t-test

dist_a = [1,2,3]
dist_b = [4,5,6]

# Z-test: Checking if the distribution means (ages of survivors vs ages of non-survivors) are statistically different
t_stat, p_value = ztest(dist_a, dist_b)
print("----- Z Test Results -----")
print("T stat. = " + str(t_stat))
print("P value = " + str(p_value)) # P-value is less than 0.05

print("")

# T-test: Checking if the distribution means (ages of survivors vs ages of non-survivors) are statistically different
t_stat_2, p_value_2 = stats.ttest_ind(dist_a, dist_b)
print("----- T Test Results -----")
print("T stat. = " + str(t_stat_2))
print("P value = " + str(p_value_2)) # P-value is less than 0.05


