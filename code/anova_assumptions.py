import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import pingouin


# anova assumptions: 
# - normality -> dv should be normally distributed for each 
#   group (level of within subject factor)
# - sphericity -> variances of the differences between all combinations 
#   of related groups (levels) should be equal
# - independence -> in repeated measures designs, this applies to the 
#   independence of different subjects rather than within-subject measurements

# normality of differences

file_path = '../results/df_hypothesis3and4.csv'
df = pd.read_csv(file_path)

def check_normality(df, group_cols, value_col):
    grouped = df.groupby(group_cols)
    for name, group in grouped:
        print(f'Checking normality for group: {name}')
        shapiro_test = stats.shapiro(group[value_col])
        print(f'Shapiro-Wilk test p-value: {shapiro_test.pvalue}')
        
        plt.figure(figsize=(8, 6))
        stats.probplot(group[value_col], dist="norm", plot=plt)
        plt.title(f'Q-Q plot for group: {name}')
        plt.show()

# check normality for each combination of 'condition' and 'stimulus type'
check_normality(df, ['condition', 'stimulus type'], 'peak magnitude')

# Mauchly's test for sphericity

sphericity_result = pingouin.sphericity(data=df, dv='peak magnitude', 
                    within=['condition', 'stimulus type'],
                    subject='participant',
                    method='mauchly', alpha=0.05)
pd.set_option('display.max_columns', None)
print(sphericity_result)

# (True, nan, nan, 1, 1.0) 